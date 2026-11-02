# TP 5 — Du texte aux vecteurs

**Durée : 1 heure.** Notebook : `tp5_etudiant.ipynb`. Données : `data/`.

## Objectifs

À la fin du TP, vous devez être capable de :

1. justifier chaque étape de prétraitement et **mesurer** son effet ;
2. construire une représentation BoW puis TF-IDF et classer une requête ;
3. provoquer et expliquer un **vecteur nul** ;
4. inspecter des embeddings pré-entraînés et expliquer un **échec**.

## Déroulé

### Bloc 1 — Prétraitement (15 min)

Complétez `normalize()` puis `tokenize()`. Mesurez le nombre de tokens, de formes distinctes, puis le même calcul après retrait des stop words.

**Rendu attendu** : les quatre nombres affichés + réponses aux trois questions.

### Bloc 2 — BoW, TF-IDF, cosinus (20 min)

Construisez la matrice documents × termes, classez la requête `le chat dort sur le canapé`, puis refaites le classement en TF-IDF. Terminez par la requête `animal de compagnie`.

**Rendu attendu** : les deux classements, la norme du vecteur de la requête inconnue, et l'explication.

### Bloc 3 — Embeddings (12 min)

Chargez `data/embeddings_fr_mini.vec`. Affichez les plus proches voisins de `chat` et `voiture`, testez deux analogies, puis inspectez `avocat`.

**Rendu attendu** : les voisins obtenus, une analogie réussie, un échec expliqué.

## Ce qui est évalué

| Critère | Poids |
|---|---|
| Fonctions correctes et lisibles | 30 % |
| Mesures et interprétations justes | 30 % |
| Explication du vecteur nul | 20 % |
| Analyse critique des embeddings | 20 % |

## Rappel

Le recopiage de sortie sans exécution ne rapporte rien : chaque réponse doit être appuyée par une cellule exécutée.
