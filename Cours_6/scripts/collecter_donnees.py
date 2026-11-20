#!/usr/bin/env python3
"""Collecte reproductible des trois sources de l'atelier patrimoine/RAG.

Exécution depuis la racine de l'atelier :
    python scripts/collecter_donnees.py

Le script privilégie les API publiques et met chaque réponse en cache. Il ne
contourne aucune protection. Les pages POP sont servies publiquement avec leurs
notices structurées intégrées ; seules les notices reliées par Wikidata (P380)
sont collectées. La sortie pédagogique est donc un sous-ensemble documenté, pas
un recensement exhaustif du patrimoine réunionnais.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html as html_lib
import json
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote, unquote

import requests
from lxml import html

RACINE = Path(__file__).resolve().parents[1]
DONNEES = RACINE / "data"
CACHE = DONNEES / "cache"
BRUTES = DONNEES / "brutes"
IMAGES = BRUTES / "images"
USER_AGENT = "AtelierPedagogiqueDataMining-RAG/1.0 (cours Esiroi; usage enseignement)"
ENDPOINT_WDQS = "https://query.wikidata.org/sparql"
API_WIKIDATA = "https://www.wikidata.org/w/api.php"
API_WIKIPEDIA = "https://fr.wikipedia.org/w/api.php"
API_COMMONS = "https://commons.wikimedia.org/w/api.php"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, deflate"})

REQUETE_INDEX = """
SELECT DISTINCT ?item ?itemLabel ?itemDescription ?merimee ?article ?image ?coord WHERE {
  ?item wdt:P131* wd:Q17070 ; wdt:P380 ?merimee .
  OPTIONAL {
    ?article schema:about ?item ;
             schema:isPartOf <https://fr.wikipedia.org/> .
  }
  OPTIONAL { ?item wdt:P18 ?image. }
  OPTIONAL { ?item wdt:P625 ?coord. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en". }
}
ORDER BY ?item ?merimee
"""


def maintenant() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ecrire_json(path: Path, objet: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(objet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ecrire_jsonl(path: Path, lignes: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for ligne in lignes:
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")


def requete(url: str, *, params: dict[str, Any] | None = None, cache: Path | None = None,
            timeout: int = 60, binaire: bool = False, essais: int = 5) -> Any:
    """GET borné, avec cache, ralentissement et respect de Retry-After."""
    if cache and cache.exists() and cache.stat().st_size > 0:
        return cache.read_bytes() if binaire else cache.read_text(encoding="utf-8")
    derniere: Exception | None = None
    for essai in range(essais):
        try:
            reponse = SESSION.get(url, params=params, timeout=timeout)
            reponse.raise_for_status()
            contenu = reponse.content if binaire else reponse.text
            if cache:
                cache.parent.mkdir(parents=True, exist_ok=True)
                if binaire:
                    cache.write_bytes(contenu)
                else:
                    cache.write_text(contenu, encoding="utf-8")
            # Une requête environ toutes les 0,4 s : sobriété pour les API publiques.
            time.sleep(0.4)
            return contenu
        except (requests.RequestException, OSError) as exc:
            derniere = exc
            if essai + 1 < essais:
                attente = 5.0 * (2 ** essai)
                reponse = getattr(exc, "response", None)
                if reponse is not None and reponse.status_code in (429, 503):
                    try:
                        attente = max(attente, float(reponse.headers.get("Retry-After", "0")))
                    except ValueError:
                        pass
                print(f"Nouvelle tentative dans {attente:.0f}s après {type(exc).__name__}: {url}", flush=True)
                time.sleep(attente)
    raise RuntimeError(f"Échec GET {url} après {essais} essais : {derniere}")


def appeler_json(url: str, params: dict[str, Any], cache: Path, timeout: int = 60) -> dict[str, Any]:
    texte = requete(url, params=params, cache=cache, timeout=timeout)
    return json.loads(texte)


def morceaux(seq: list[Any], taille: int) -> Iterable[list[Any]]:
    for debut in range(0, len(seq), taille):
        yield seq[debut:debut + taille]


def texte_html(valeur: Any) -> str:
    """Convertit une valeur de métadonnée MediaWiki éventuellement riche en texte."""
    if valeur is None:
        return ""
    if isinstance(valeur, dict):
        valeur = valeur.get("value", "")
    if not isinstance(valeur, str):
        return str(valeur)
    try:
        fragment = html.fragment_fromstring(valeur, create_parent=True)
        texte = fragment.text_content()
    except (ValueError, TypeError):
        texte = html_lib.unescape(re.sub(r"<[^>]+>", " ", valeur))
    return re.sub(r"\s+", " ", html_lib.unescape(texte)).strip()


def slug(texte: str, maximum: int = 65) -> str:
    normalise = unicodedata.normalize("NFKD", texte)
    ascii_ = normalise.encode("ascii", "ignore").decode("ascii").lower()
    propre = re.sub(r"[^a-z0-9]+", "-", ascii_).strip("-")
    return (propre[:maximum].strip("-") or "fichier")


def collecter_index(max_edifices: int | None = None) -> list[dict[str, Any]]:
    donnees = appeler_json(
        ENDPOINT_WDQS,
        {"query": REQUETE_INDEX, "format": "json"},
        CACHE / "wikidata" / "index_reunion.json",
        timeout=120,
    )
    lignes = donnees["results"]["bindings"]
    regroupe: dict[str, dict[str, Any]] = {}
    for ligne in lignes:
        valeur = {cle: champ.get("value") for cle, champ in ligne.items()}
        qid = valeur["item"].rsplit("/", 1)[-1]
        entree = regroupe.setdefault(qid, {
            "qid": qid,
            "url_wikidata": valeur["item"],
            "label": valeur.get("itemLabel") or qid,
            "description_wikidata": valeur.get("itemDescription") or "",
            "ids_merimee": [],
            "article_url": valeur.get("article") or "",
            "images": [],
            "coordonnees": [],
        })
        if valeur.get("itemDescription") and not entree["description_wikidata"]:
            entree["description_wikidata"] = valeur["itemDescription"]
        if valeur.get("merimee") and valeur["merimee"] not in entree["ids_merimee"]:
            entree["ids_merimee"].append(valeur["merimee"])
        if valeur.get("article_url") and not entree["article_url"]:
            entree["article_url"] = valeur["article_url"]
        if valeur.get("image") and valeur["image"] not in entree["images"]:
            entree["images"].append(valeur["image"])
        if valeur.get("coord") and valeur["coord"] not in entree["coordonnees"]:
            entree["coordonnees"].append(valeur["coord"])
    index = sorted(regroupe.values(), key=lambda x: (x["ids_merimee"][0], x["qid"]))
    if max_edifices is not None:
        index = index[:max_edifices]
    return index


def parser_notice_pop(page: str, reference: str) -> dict[str, Any]:
    """Extrait l'objet notice présent dans les fragments React Server Components.

    Ce parseur refuse silencieusement-faux : si l'objet de la bonne référence est
    absent, il lève une erreur plutôt que de produire une notice vide.
    """
    decodeur = json.JSONDecoder()
    morceaux_vus: list[str] = []
    for match in re.finditer(r"<script[^>]*>(self\.__next_f\.push\(.*?\))</script>", page, re.S):
        appel = match.group(1)
        debut = appel.find("(")
        try:
            payload = json.loads(appel[debut + 1:-1])
        except (json.JSONDecodeError, ValueError):
            continue
        if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], str):
            continue
        fragment = payload[1]
        morceaux_vus.append(fragment)
        depart = 0
        while True:
            position = fragment.find('"notice":', depart)
            if position < 0:
                break
            try:
                objet, _ = decodeur.raw_decode(fragment, position + len('"notice":'))
            except json.JSONDecodeError:
                depart = position + 1
                continue
            if isinstance(objet, dict) and objet.get("REF") == reference:
                return objet
            depart = position + 1
    # Certains découpages peuvent répartir les fragments ; dernier essai sur le flux joint.
    flux = "".join(morceaux_vus)
    for position in [m.start() for m in re.finditer(r'"notice":', flux)]:
        try:
            objet, _ = decodeur.raw_decode(flux, position + len('"notice":'))
        except json.JSONDecodeError:
            continue
        if isinstance(objet, dict) and objet.get("REF") == reference:
            return objet
    raise ValueError(f"Objet notice {reference} introuvable dans la page POP ({len(page)} octets)")


def collecter_pop(index: list[dict[str, Any]], collecte: str) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    erreurs: list[dict[str, str]] = []
    sorties: dict[str, dict[str, Any]] = {}
    refs = sorted({ref for item in index for ref in item["ids_merimee"]})
    for i, ref in enumerate(refs, 1):
        url = f"https://pop.culture.gouv.fr/notice/merimee/{quote(ref)}"
        try:
            page = requete(url, cache=CACHE / "pop" / f"{ref}.html", timeout=45)
            notice = parser_notice_pop(page, ref)
            sorties[ref] = {
                "source": "POP/Mérimée",
                "source_id": ref,
                "url": url,
                "date_collecte": collecte,
                "statut_collecte": "disponible",
                "notice": notice,
            }
        except Exception as exc:  # absence explicite et traçable, pas de ligne fictive
            erreurs.append({"source": "POP", "id": ref, "url": url, "erreur": str(exc)})
            sorties[ref] = {
                "source": "POP/Mérimée",
                "source_id": ref,
                "url": url,
                "date_collecte": collecte,
                "notice": None,
                "statut_collecte": "indisponible",
                "erreur_collecte": str(exc),
            }
        if i % 25 == 0 or i == len(refs):
            print(f"POP : {i}/{len(refs)} notices lues, {len(erreurs)} erreurs", flush=True)
    return list(sorties.values()), erreurs


def titre_depuis_url(url: str) -> str:
    if "/wiki/" not in url:
        return ""
    return unquote(url.rsplit("/wiki/", 1)[1]).replace("_", " ")


def collecter_textes_wikipedia(index: list[dict[str, Any]], erreurs: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    par_titre: dict[str, str] = {}
    for item in index:
        titre = titre_depuis_url(item["article_url"])
        if titre:
            par_titre[titre] = item["qid"]
    resultats: dict[str, dict[str, Any]] = {}
    titres = sorted(par_titre)
    for i, groupe in enumerate(morceaux(titres, 20), 1):
        params = {
            "action": "query", "format": "json", "formatversion": "2",
            "prop": "extracts|info", "explaintext": "1", "exlimit": "1",
            "inprop": "url", "redirects": "1", "titles": "|".join(groupe),
        }
        # MediaWiki abaisse exlimit à 1 pour les textes entiers. Il faut suivre
        # excontinue jusqu'à épuisement : une page sans extract lors du premier
        # appel n'est PAS un article vide.
        continuation = 0
        empreinte_requete = hashlib.sha1("|".join(groupe).encode("utf-8")).hexdigest()[:10]
        while True:
            cache = CACHE / "wikipedia" / (f"articles_{i:02d}_{empreinte_requete}.json" if continuation == 0 else f"articles_{i:02d}_{empreinte_requete}_cont_{continuation:02d}.json")
            try:
                donnees = appeler_json(API_WIKIPEDIA, params, cache, timeout=60)
            except Exception as exc:
                erreurs.append({"source": "Wikipédia", "id": f"lot {i}, continuation {continuation}", "url": API_WIKIPEDIA, "erreur": str(exc)})
                break
            for page in donnees.get("query", {}).get("pages", []):
                titre_original = page.get("title", "")
                precedent = resultats.get(titre_original, {})
                nouveau_texte = page.get("extract")
                resultats[titre_original] = {
                    "titre": titre_original,
                    "texte_integral": nouveau_texte if nouveau_texte is not None else precedent.get("texte_integral", ""),
                    "url_wikipedia": page.get("fullurl", "") or precedent.get("url_wikipedia", ""),
                    "pageid_wikipedia": page.get("pageid") or precedent.get("pageid_wikipedia"),
                    "manquant": bool(page.get("missing", False)),
                }
            for redirection in donnees.get("query", {}).get("redirects", []):
                cible = redirection.get("to")
                if cible in resultats:
                    resultats[redirection.get("from", "")] = resultats[cible]
            prochain = donnees.get("continue", {}).get("excontinue")
            if prochain is None:
                break
            continuation += 1
            if continuation > len(groupe) + 2:
                erreurs.append({"source": "Wikipédia", "id": f"lot {i}", "url": API_WIKIPEDIA, "erreur": "Continuation anormalement longue"})
                break
            params["excontinue"] = prochain
        print(f"Wikipédia : lot {i}, {len(resultats)} titres indexés, {sum(bool(x['texte_integral']) for x in resultats.values())} textes", flush=True)
    return resultats


def collecter_aliases(index: list[dict[str, Any]], erreurs: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    resultats: dict[str, dict[str, Any]] = {}
    qids = [x["qid"] for x in index]
    for i, groupe in enumerate(morceaux(qids, 50), 1):
        params = {
            "action": "wbgetentities", "format": "json", "formatversion": "2",
            "props": "labels|aliases|descriptions", "languages": "fr|en",
            "ids": "|".join(groupe),
        }
        try:
            donnees = appeler_json(API_WIKIDATA, params, CACHE / "wikidata" / f"entites_{i:02d}.json")
        except Exception as exc:
            erreurs.extend({"source": "Wikidata", "id": qid, "url": API_WIKIDATA, "erreur": str(exc)} for qid in groupe)
            continue
        entites = donnees.get("entities", {})
        if isinstance(entites, list):
            entites = {x["id"]: x for x in entites}
        for qid, entite in entites.items():
            def libelles(cle: str) -> dict[str, str]:
                return {langue: val.get("value", "") for langue, val in entite.get(cle, {}).items()}
            aliases = entite.get("aliases", {})
            resultats[qid] = {
                "labels": libelles("labels"),
                "descriptions": libelles("descriptions"),
                "alias_fr": [x.get("value", "") for x in aliases.get("fr", [])],
                "alias_en": [x.get("value", "") for x in aliases.get("en", [])],
            }
    return resultats


def assembler_source2(index: list[dict[str, Any]], collecte: str) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    erreurs: list[dict[str, str]] = []
    textes = collecter_textes_wikipedia(index, erreurs)
    aliases = collecter_aliases(index, erreurs)
    # Même après un échec ponctuel, toutes les entités de l'index restent présentes ;
    # les champs absents demeurent vides et l'erreur est publiée dans le journal.
    lignes = []
    for item in index:
        titre = titre_depuis_url(item["article_url"])
        article = textes.get(titre, {})
        meta = aliases.get(item["qid"], {})
        lignes.append({
            "source": "Wikidata/Wikipédia",
            "source_id": item["qid"],
            "ids_merimee_declares": item["ids_merimee"],
            "url_wikidata": item["url_wikidata"],
            "url_wikipedia": article.get("url_wikipedia") or item["article_url"],
            "titre_wikipedia": article.get("titre") or titre,
            "label_wikidata": meta.get("labels", {}).get("fr") or item["label"],
            "labels_wikidata": meta.get("labels", {}),
            "description_wikidata": meta.get("descriptions", {}).get("fr") or item["description_wikidata"],
            "descriptions_wikidata": meta.get("descriptions", {}),
            "alias_fr": meta.get("alias_fr", []),
            "alias_en": meta.get("alias_en", []),
            "texte_integral": article.get("texte_integral", ""),
            "article_present": bool(article.get("texte_integral")),
            "article_manquant": article.get("manquant", False),
            "coordonnees_wikidata": item["coordonnees"],
            "images_declarees": item["images"],
            "date_collecte": collecte,
        })
    return lignes, erreurs


def fichier_depuis_url(url: str) -> str:
    marqueur = "Special:FilePath/"
    if marqueur in url:
        return "File:" + unquote(url.rsplit(marqueur, 1)[1]).replace("_", " ")
    if "/wiki/File:" in url:
        return "File:" + unquote(url.rsplit("/wiki/File:", 1)[1])
    return "File:" + unquote(url.rsplit("/", 1)[-1]).replace("_", " ")


def collecter_commons(index: list[dict[str, Any]], collecte: str, telecharger: bool = True) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    liens: dict[str, set[str]] = {}
    for item in index:
        for url_image in item["images"]:
            titre = fichier_depuis_url(url_image)
            liens.setdefault(titre, set()).add(item["qid"])
    titres = sorted(liens)
    infos: dict[str, dict[str, Any]] = {}
    erreurs: list[dict[str, str]] = []
    for i, groupe in enumerate(morceaux(titres, 20), 1):
        params = {
            "action": "query", "format": "json", "formatversion": "2", "prop": "imageinfo",
            "iiprop": "url|sha1|size|mime|extmetadata", "iiurlwidth": "900",
            "iiextmetadatalanguage": "fr",
            "iiextmetadatafilter": "ImageDescription|Artist|Credit|LicenseShortName|LicenseUrl|UsageTerms|Attribution|Copyrighted|DateTime|Categories|ObjectName",
            "titles": "|".join(groupe),
        }
        try:
            donnees = appeler_json(API_COMMONS, params, CACHE / "commons" / f"images_{i:02d}.json")
        except Exception as exc:
            erreurs.extend({"source": "Commons", "id": t, "url": "", "erreur": str(exc)} for t in groupe)
            continue
        for page in donnees.get("query", {}).get("pages", []):
            if page.get("missing") or not page.get("imageinfo"):
                erreurs.append({"source": "Commons", "id": page.get("title", ""), "url": "", "erreur": "fichier absent"})
                continue
            infos[page["title"]] = page
        print(f"Commons : lot {i}, {len(infos)} fichiers trouvés", flush=True)

    lignes: list[dict[str, Any]] = []
    chemins: dict[str, str] = {}
    for numero, titre in enumerate(titres, 1):
        page = infos.get(titre)
        if not page:
            continue
        info = page["imageinfo"][0]
        meta = info.get("extmetadata", {})
        pageid = str(page.get("pageid") or hashlib.sha1(titre.encode()).hexdigest()[:12])
        mime = info.get("thumbmime") or info.get("mime") or "image/jpeg"
        extension = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}.get(mime, ".jpg")
        relatif = f"data/brutes/images/{pageid}_{slug(titre.removeprefix('File:'))}{extension}"
        destination = RACINE / relatif
        if telecharger and titre not in chemins:
            url_telechargement = info.get("thumburl") or info.get("url")
            try:
                contenu = requete(
                    url_telechargement,
                    cache=CACHE / "fichiers" / destination.name,
                    timeout=75, binaire=True,
                )
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(contenu)
                chemins[titre] = relatif
            except Exception as exc:
                erreurs.append({"source": "Commons/image", "id": titre, "url": url_telechargement, "erreur": str(exc)})
                continue
            if numero % 30 == 0 or numero == len(titres):
                print(f"Images : {numero}/{len(titres)} fichiers traités, {len(erreurs)} erreurs cumulées", flush=True)
        chemin = chemins.get(titre, relatif if destination.exists() else "")
        for qid in sorted(liens[titre]):
            lignes.append({
                "source": "Wikimedia Commons",
                "image_id": pageid,
                "qid": qid,
                "titre_fichier": titre,
                "chemin_local": chemin,
                "url_page_description": info.get("descriptionurl", ""),
                "url_original": info.get("url", ""),
                "url_vignette": info.get("thumburl", ""),
                "largeur": info.get("width"),
                "hauteur": info.get("height"),
                "taille_octets_originale": info.get("size"),
                "mime_original": info.get("mime", ""),
                "sha1_commons_original": info.get("sha1", ""),
                "description_commons": texte_html(meta.get("ImageDescription") or meta.get("ObjectName")),
                "auteur": texte_html(meta.get("Artist") or meta.get("Attribution")),
                "credit": texte_html(meta.get("Credit")),
                "licence": texte_html(meta.get("LicenseShortName") or meta.get("UsageTerms")),
                "licence_url": texte_html(meta.get("LicenseUrl")),
                "date_fichier": texte_html(meta.get("DateTime")),
                "categories": texte_html(meta.get("Categories")),
                "date_collecte": collecte,
            })
    return lignes, erreurs


def ecrire_csv(path: Path, lignes: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    colonnes = list(lignes[0]) if lignes else ["source", "image_id", "qid", "titre_fichier"]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=colonnes, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(lignes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-edifices", type=int, default=None, help="limite de test (défaut : toutes les notices)")
    parser.add_argument("--sans-images", action="store_true", help="métadonnées Commons seulement")
    args = parser.parse_args()
    (BRUTES / "images").mkdir(parents=True, exist_ok=True)
    collecte = maintenant()
    print("1/4 Index Wikidata", flush=True)
    index = collecter_index(args.max_edifices)
    ecrire_json(BRUTES / "index_liaison.json", index)
    print(f"Index : {len(index)} entités, {sum(len(x['ids_merimee']) for x in index)} références Mérimée", flush=True)

    print("2/4 POP/Mérimée", flush=True)
    source1, erreurs1 = collecter_pop(index, collecte)
    ecrire_jsonl(BRUTES / "source_1_pop_merimee.jsonl", source1)

    print("3/4 Wikidata/Wikipédia", flush=True)
    source2, erreurs2 = assembler_source2(index, collecte)
    ecrire_jsonl(BRUTES / "source_2_wikidata_wikipedia.jsonl", source2)

    print("4/4 Wikimedia Commons", flush=True)
    source3, erreurs3 = collecter_commons(index, collecte, telecharger=not args.sans_images)
    ecrire_csv(BRUTES / "source_3_commons.csv", source3)

    erreurs = erreurs1 + erreurs2 + erreurs3
    ecrire_csv(BRUTES / "erreurs_collecte.csv", erreurs)
    manifeste = {
        "date_collecte": collecte,
        "perimetre": "Entités Wikidata situées dans La Réunion (P131*) et porteuses d'une référence Mérimée (P380). Sous-ensemble non exhaustif.",
        "user_agent": USER_AGENT,
        "comptes": {
            "entites_index": len(index),
            "references_merimee_uniques": len({r for x in index for r in x["ids_merimee"]}),
            "references_pop_suivies": len(source1),
            "notices_pop_disponibles": sum(x.get("notice") is not None for x in source1),
            "references_pop_indisponibles": sum(x.get("notice") is None for x in source1),
            "entites_wikidata_wikipedia": len(source2),
            "articles_wikipedia_avec_texte": sum(bool(x.get("texte_integral")) for x in source2),
            "lignes_commons_entite_image": len(source3),
            "fichiers_images_uniques": len({x.get("image_id") for x in source3}),
            "associations_avec_image_locale": sum(bool(x.get("chemin_local")) for x in source3),
            "fichiers_images_locaux_uniques": len({x.get("chemin_local") for x in source3 if x.get("chemin_local")}),
        },
        "sources": {
            "wikidata_query": ENDPOINT_WDQS,
            "wikidata_api": API_WIKIDATA,
            "wikipedia_api": API_WIKIPEDIA,
            "commons_api": API_COMMONS,
            "pop_url_modele": "https://pop.culture.gouv.fr/notice/merimee/{REF}",
        },
        "erreurs": len(erreurs),
        "images_telechargees": not args.sans_images,
        "versions": {"python_requests": requests.__version__},
    }
    ecrire_json(BRUTES / "manifeste_collecte.json", manifeste)
    print(json.dumps(manifeste["comptes"], ensure_ascii=False, indent=2), flush=True)
    print(f"Collecte terminée : {manifeste['erreurs']} erreur(s), voir data/brutes/erreurs_collecte.csv", flush=True)


if __name__ == "__main__":
    main()
