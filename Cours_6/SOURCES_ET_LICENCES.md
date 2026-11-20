# Sources, périmètre et licences

## Périmètre du corpus

La collecte part d’une requête Wikidata : entités situées dans La Réunion (`P131*`) et porteuses d’une référence Mérimée (`P380`). Cette méthode permet de relier proprement les trois sources, mais **ne constitue pas un recensement exhaustif du patrimoine réunionnais**.

Les notices POP sont limitées aux références trouvées dans cet index. Les textes Wikipédia sont limités aux articles français reliés. Les médias sont les images principales déclarées avec Wikidata `P18`, pas toutes les photographies disponibles dans Commons.

Les dates d’édition et de collecte sont distinctes. Toute nouvelle exécution peut modifier les contenus, liens, licences et compteurs. Le manifeste fige la version utilisée en classe.

## Sources officielles et documentation

| Source | Utilisation | Liens |
|---|---|---|
| **POP — Plateforme ouverte du patrimoine** | notices Mérimée et champs structurés | [POP](https://pop.culture.gouv.fr/) · [Présentation par le ministère de la Culture](https://www.culture.gouv.fr/rechercher-une-publication-du-ministere-de-la-culture/bases-de-donnees/la-plate-forme-ouverte-du-patrimoine-pop) |
| **Wikidata** | index géographique, P380, QID, labels, alias, images P18, coordonnées | [Propriété P380 — identifiant Mérimée](https://www.wikidata.org/wiki/Property:P380) · [Aide SPARQL](https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/Wikidata_Query_Help/fr) |
| **Wikipédia francophone** | titres, URL et articles en texte intégral via l’Action API | [API REST Wikimedia — contexte général](https://www.mediawiki.org/wiki/Wikimedia_REST_API) · [Recherche Action API](https://www.mediawiki.org/wiki/API:Search) |
| **Wikimedia Commons** | vignettes, descriptions, auteurs et licences par fichier | [API Imageinfo](https://www.mediawiki.org/wiki/API:Imageinfo) · [Données lisibles par machine](https://commons.wikimedia.org/wiki/Commons:Machine-readable_data) |

Le collecteur utilise `requests`, un `User-Agent` descriptif, un cache local, des temps d’attente et `Retry-After`. Aucun contrôle CAPTCHA, mécanisme anti-robot ou restriction d’accès n’est contourné.

## Cas d’erreur conservés volontairement

Le fichier `data/brutes/erreurs_collecte.csv` est un journal, pas une annexe décorative. Il signale notamment toute référence POP suivie par Wikidata dont la notice est indisponible. La ligne suivie est conservée avec `statut_collecte = indisponible`, sans faux contenu.

Lors de l’extraction Wikipédia, les articles entiers sont paginés : le champ `excontinue` doit être suivi jusqu’à épuisement. Une première page sans `extract` ne signifie donc pas « article vide ». Le collecteur compte séparément les titres lus et les textes rattachés.

## Licences et attribution

### POP / Mérimée

Le site POP indique une licence Etalab-2.0 pour ses contenus, **sauf mention explicite de propriété intellectuelle détenue par des tiers**. Les mentions légales d’une notice restent dans les données lorsqu’elles existent. Le champ licence des chunks renvoie à cette précaution et ne remplace pas une vérification de la notice.

### Wikidata et Wikipédia

Les métadonnées Wikidata sont marquées `CC0`. Le texte Wikipédia n’est **pas** traité comme du CC0 : les conditions de réutilisation du texte, l’attribution et l’historique de la page doivent être préservés. Voir les [conditions d’utilisation Wikimedia](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use) et la [page de licence Wikidata](https://www.wikidata.org/wiki/Wikidata:Licensing).

Le corpus distingue donc les chunks `Wikidata` des chunks `Wikipédia`, même si leur `entity_id` est commun.

### Wikimedia Commons

Chaque image possède ses propres informations : page descriptive, auteur déclaré, crédit, licence et URL de licence. La disponibilité d’une image sur Internet n’implique pas une licence unique. Ne pas agréger les licences des images dans une seule ligne de corpus.

Le fichier `ATTRIBUTIONS_COMMONS.csv` doit accompagner toute diffusion du dossier d’images et de ses variantes pédagogiques. Pour une publication au-delà de la salle de classe, revoir chaque page descriptive et chaque obligation de partage à l’identique.

## Transformations pédagogiques

Les fichiers de `data/atelier/` comportent certaines anomalies **clairement séparées des bruts** :

- copies techniques de lignes ;
- P380 masqués sur un sous-ensemble ;
- copie binaire de quatre images ;
- redimensionnement/récompression de quatre autres images.

Ces opérations n’apportent aucune information historique nouvelle. Elles servent à tester les décisions. Les variantes d’images sont réalisées à partir de Commons et conservent les champs auteur/licence/source de l’original ; la table d’attributions précise leur caractère dérivé.

## Règles RAG retenues

- Un chunk = une source principale.
- `entity_id` interne ne remplace pas `source_id`.
- `chunk_id` contient source, entité, position et texte via une empreinte : deux sources ne partagent pas un ID du seul fait d’un même texte.
- `parents_ids` relie une projection structurée aux chunks sources.
- `mode_production` distingue données d’origine, métadonnées, transformation déterministe, annotation humaine et modèle génératif.
- `est_synthetique` est `False` dans le socle, y compris pour les templates déterministes. Une sortie de modèle génératif impose un autre traitement et une revue, pas une simple modification de libellé.
- Une description Commons reste une affirmation sourcée, pas une validation visuelle.
- Les conflits et liens incertains restent visibles ; il n’y a pas de « vote majoritaire » silencieux.

## Limite de l’évaluation

Les liens P380 servent de référence pédagogique pour mesurer les décisions automatiques. Ils ne constituent pas une annotation humaine indépendante de chaque identité. Les questions de retrieval disposent d’une cible par question pour ce petit protocole ; elles ne couvrent pas tous les besoins documentaires possibles.

Les rotations, recadrages et réencodages peuvent tester un modèle visuel ou un détecteur de doublons. **Ils ne constituent pas, à eux seuls, une augmentation sémantique utile d’un index RAG textuel.**
