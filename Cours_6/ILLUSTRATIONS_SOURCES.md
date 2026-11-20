# Illustrations de l’atelier — sources et licences

Toutes les illustrations sont stockées localement dans `illustrations_etapes/` et intégrées au notebook sans accès Internet. Les textes alternatifs figurent dans le notebook.

**Typographie :** les textes des illustrations générées utilisent DejaVu Sans pour préserver correctement les caractères accentués. La police figure dans `assets/fonts/DejaVuSans.ttf`, avec sa licence dans `assets/fonts/LICENCE_DEJAVU.txt`.

## Illustrations externes

| Étape | Fichier local | Auteur / source | Licence | Page descriptive |
|---|---|---|---|---|
| collecte via API | `illustrations_etapes/00_collecte_api.png` | I.hate.spam.mail.here | CC0 | [File:Web API diagram.svg](https://commons.wikimedia.org/wiki/File:Web_API_diagram.svg) |
| normalisation Unicode (logo) | `illustrations_etapes/02_unicode.png` | Unicode Consortium | Public domain | [File:New Unicode logo.svg](https://commons.wikimedia.org/wiki/File:New_Unicode_logo.svg) |
| distance d’édition (archive) | `illustrations_etapes/03_levenshtein.gif` | Napsternxg | CC BY-SA 4.0 | [File:Levenshtein distance animation.gif](https://commons.wikimedia.org/wiki/File:Levenshtein_distance_animation.gif) |
| retrieval et provenance | `illustrations_etapes/06_catalogue_bibliotheque.png` | General Services Administration. National Archives and Records Service. Office of Educational Programs. Education Division. ?-4/1/1985 | Public domain | [File:Photograph of Card Catalog in Central Search Room - DPLA - 5be4fa7f7ec7f58594a5dc6765659025.jpg](https://commons.wikimedia.org/wiki/File:Photograph_of_Card_Catalog_in_Central_Search_Room_-_DPLA_-_5be4fa7f7ec7f58594a5dc6765659025.jpg) |
| comparaison TF-IDF et cosinus | `illustrations_etapes/07_cosine.png` | Renepick | CC BY-SA 3.0 | [File:Cosine-Similarity-For-Vectorspaces.pdf](https://commons.wikimedia.org/wiki/File:Cosine-Similarity-For-Vectorspaces.pdf) |
| pHash avant/après | `illustrations_etapes/05_phash_avant_apres.png` | Thierry Caro + variante pédagogique | CC BY-SA 3.0 | [File:Domaine-de-Clermont.jpg](https://commons.wikimedia.org/wiki/File:Domaine-de-Clermont.jpg) |

## Schémas pédagogiques composés pour le cours

Ces schémas ont été créés pour l’atelier (texte + formes) avec DejaVu Sans. Ils n’introduisent aucune donnée visuelle nouvelle hors exemples tirés du corpus.

| Étape | Fichier local | Contenu |
|---|---|---|
| profilage | `01_profilage_sources.png` | Compteurs extraits du manifeste de la collecte |
| Unicode NFC / NFKD | `02_unicode_explique.png` | Forme recollée vs forme détachée de la lettre « é » |
| copies techniques | `03_copie_technique.png` | Original vs photocopie, même empreinte SHA-256 |
| homonymes | `03_homonymes.png` | Quatre notices « Maison » à des adresses différentes |
| rapprochement | `04_rapprochement_entites.png` | Deux carnets d’adresses reliés (POP ↔ Wikidata) |
| Levenshtein + Jaccard | `04_levenshtein_jaccard.png` | Complémentarité des deux mesures sur titres courts |
| marge | `04_marge_candidats.png` | Cas douteux (`a_revoir`) vs cas net (`automatique`) |

Les attributions complètes des images du corpus restent dans `ATTRIBUTIONS_COMMONS.csv`. Les photos de l’atelier sont accessibles publiquement : cela ne signifie pas qu’elles soient dans le domaine public.
