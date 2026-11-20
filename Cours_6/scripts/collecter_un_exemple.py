#!/usr/bin/env python3
"""Mini-collecte pédagogique : une entité seulement, hors ligne par défaut.

Sans option : inspecte l'exemple figé dans data/atelier/exemple_collecte.json.
Avec --en-ligne : exécute une petite collecte réelle pour l'entité choisie.
Le scraping massif n'est pas un objectif de l'atelier. Respecter les API, le
cache, l'identification User-Agent et le débit ; ne pas relancer en parallèle.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from scripts.collecter_donnees import (  # noqa: E402
    collecter_index, collecter_pop, assembler_source2, collecter_commons,
    maintenant,
)


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--en-ligne", action="store_true", help="effectue les requêtes réseau miniature")
    parser.add_argument("--qid", default="", help="QID à collecter ; défaut : celui de l'exemple figé")
    args = parser.parse_args()
    exemple_path = RACINE / "data" / "atelier" / "exemple_collecte.json"
    exemple = json.loads(exemple_path.read_text(encoding="utf-8"))
    qid = args.qid or exemple["qid"]
    if not args.en_ligne:
        print("MODE HORS LIGNE — réponse brute figée, aucune requête réseau")
        print("QID :", qid)
        print("1. POP :", len(exemple["source_1_pop"]), "notice(s) ; clés :", list(exemple["source_1_pop"][0])[:8])
        print("2. Wikidata/Wikipédia :", exemple["source_2_wikidata_wikipedia"]["source_id"], ";", len(exemple["source_2_wikidata_wikipedia"].get("texte_integral", "")), "caractères")
        print("3. Commons :", len(exemple["source_3_commons"]), "association(s) image ; licences :", sorted({x.get("licence", "") for x in exemple["source_3_commons"]}))
        print("Observez 'date_collecte', les URL et les licences. Pour rejouer : --en-ligne")
        return
    print("MODE EN LIGNE — une seule entité, débit limité et cache activés")
    item = next((x for x in collecter_index() if x["qid"] == qid), None)
    if item is None:
        raise SystemExit(f"QID {qid} absent du périmètre documenté")
    maintenant_collecte = maintenant()
    source1, erreurs1 = collecter_pop([item], maintenant_collecte)
    source2, erreurs2 = assembler_source2([item], maintenant_collecte)
    source3, erreurs3 = collecter_commons([item], maintenant_collecte, telecharger=False)
    sortie = {
        "qid": qid, "date_collecte": maintenant_collecte,
        "source_1_pop": source1,
        "source_2_wikidata_wikipedia": source2[0],
        "source_3_commons": source3,
        "erreurs": erreurs1 + erreurs2 + erreurs3,
    }
    destination = RACINE / "sorties" / f"collecte_directe_{qid}.json"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(sortie, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Écrit :", destination.relative_to(RACINE))
    print("Licences Commons :", sorted({x.get("licence", "") for x in source3}))
    print("Erreurs :", len(sortie["erreurs"]))


if __name__ == "__main__":
    main()
