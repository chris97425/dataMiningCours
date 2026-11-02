# TP 5 — Du texte aux vecteurs

## Contenu

| Fichier | Rôle |
|---|---|
| `tp5_enonce.md` | Énoncé distribué aux étudiants |
| `tp5_etudiant.ipynb` | Notebook à compléter |
| `tp5_corrige.ipynb` | Corrigé enseignant (exécuté) |
| `data/corpus_fr.txt` | 30 textes courts, 282 mots |
| `data/stopwords_fr.txt` | 164 mots outils français |
| `data/embeddings_fr_mini.vec` | 5 000 mots × 100 dimensions, 4,2 Mo, format texte word2vec |

## Installation

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Choix techniques

- **Aucun téléchargement pendant la séance** : le corpus, les stop words et les embeddings sont dans `data/`.
- **Pas de NLTK ni de spaCy** dans le notebook : tout le prétraitement est en `re` + `unicodedata`, conformément au cours (section S2).
- **Embeddings pré-calculés** : issus de `fr_core_news_md` (spaCy, vecteurs 300 dimensions entraînés sur du texte français), tronqués à 100 dimensions et aux 5 000 mots les plus fréquents (liste de fréquence `hermitdave/FrequencyWords`). Ils ne sont **pas** réentraînés pendant le TP : l'exercice porte sur l'inspection, pas sur l'entraînement.
- Le corpus est volontairement petit (282 mots) : les temps d'exécution sont négligeables et les effets (vocabulaire, densité, OOV) restent visibles.

## Limites assumées

- 30 textes ne suffisent pas à produire des statistiques stables : les scores TF-IDF du TP illustrent un mécanisme, pas une performance.
- Les vecteurs fournis sont généralistes : le vocabulaire spécialisé peut manquer, ce qui est précisément l'objet du bloc 3.
