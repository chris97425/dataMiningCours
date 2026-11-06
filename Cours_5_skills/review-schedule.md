# Calendrier de révision espacée — cours 5

**Méthode** : `spaced-practice-scheduler` (Cepeda et al. 2006, Roediger & Butler 2011, Rohrer et al. 2015).
**Principe non négociable** : chaque case du calendrier est une **récupération**, jamais une relecture. Relire donne une sensation de familiarité qui ne survit pas à trois semaines.

**Intervalles retenus** : J+1, J+7, J+21. Ce sont des points de départ de praticien, pas des optima mesurés. Cepeda et al. relient la durée efficace de l'intervalle à la durée de rétention visée — pas à une séquence fixe. Si le premier rappel du J+1 échoue massivement, on raccourcit ; s'il est trivial, on allonge.

---

## Le calendrier

Chaque ligne indique **ce qu'on récupère**, **quand**, et **comment**. « Réviser la section 4 » n'est pas une consigne : c'est une invitation à relire.

### J+1 — le lendemain du cours 5

| Durée | Ce qu'on récupère | Comment — la tâche exacte |
|---|---|---|
| 4 min | Les quatre sources de difficulté du langage | Feuille blanche. Écrire les quatre, avec un exemple **différent** de la slide pour chacune. Ouvrir les notes après. |
| 5 min | La matrice de Levenshtein | Remplir `chien` / `chats` sans aide. La réponse finale est 3. Si une case est fausse, refaire la ligne entière et dire pourquoi. |
| 4 min | La formule du cosinus | Écrire la formule de mémoire, puis recalculer `le chat` / D2 (réponse : 0,447) et vérifier. |
| 2 min | Le contrat | Réécrire ce que vous vous êtes engagé à faire : tentative avant explication, confiance avant vérification. |

**Total : 15 min.** À faire dans cet ordre — du plus ancien au plus récent serait une erreur : on commence par ce qui est le plus fragile.

### J+7 — une semaine après

| Durée | Ce qu'on récupère | Comment |
|---|---|---|
| 6 min | **Entrelacement S2 / S3 / S4** | Prendre une phrase jamais vue (`Le vieux chien dort près du feu, dehors.`). La prétraiter, puis dire quelle distance d'édition sépare `chien` de `chiens`, puis construire son vecteur de comptage sur un vocabulaire de 5 mots. Les trois capacités dans une seule tâche. |
| 5 min | L'IDF | Calculer de mémoire `idf` pour un mot présent dans 2 documents sur 6 (réponse : `ln(7/3)+1 ≈ 1,847`). Puis pour un mot présent dans 6 sur 6 (réponse : 1). |
| 4 min | La prédiction de classement | Reprendre `félin salon` et **écrire le classement attendu avant** de vérifier. C'est l'exercice le plus rentable du calendrier : il teste C4 en conditions de transfert. |
| 3 min | Le cas du vecteur nul | Écrire, sans notes, pourquoi `animal de compagnie` donne 0 partout — en distinguant « score de 0 » et « score indéfini ». |

**Total : 18 min.**

### J+21 — trois semaines après

| Durée | Ce qu'on récupère | Comment |
|---|---|---|
| 8 min | **Le banc d'essai des quatre requêtes** | Refaire la tâche de performance de S8 sur un corpus différent (n'importe quel jeu de textes : recettes, offres d'emploi, articles). C'est la seule mesure honnête de C6. |
| 5 min | Les quatre compréhensions durables | Les écrire de mémoire, en une phrase chacune, sans regarder. Puis comparer à `PLAN_PEDAGOGIQUE_v3.md` § Étape 1. |
| 4 min | Les trois points de blocage | Nommer, pour chacun, ce qu'un étudiant croit à tort : 2→3, 4→5, 5→6. Si vous ne retrouvez pas le troisième, relisez `PLAN_PEDAGOGIQUE_v3.md` § Progression. |

**Total : 17 min.**

---

## Entrelacement : la règle des sessions suivantes

Les cours 6 à 9 réutilisent tous le cours 5. La révision ne doit donc **pas** être un bloc séparé : elle s'insère dans l'ouverture de chaque séance suivante, 8 à 10 minutes, sur des items mélangés.

| Séance | Ouverture — récupération du cours 5 | Ce que ça prépare |
|---|---|---|
| **6** — Embeddings et Transformers | « Un mot, un vecteur : quel cas du cours 5 cela casse-t-il ? » + recalculer un cosinus entre deux phrases | L'attention comme réponse à la polysémie |
| **7** — Recherche vectorielle | « TF-IDF contre dense : lequel choisir pour `rappel@k`, et sur quel critère ? » | La baseline lexicale |
| **8** — RAG avec LangChain | « Décrire les deux phases d'un RAG, et dire où le cours 5 s'arrête » | Le plan de la chaîne |
| **9** — Évaluer et industrialiser | « Quelles limites du cours 5 deviennent des critères d'évaluation ? » | Les métriques de fidélité |

**Règle d'entrelacement** : ne jamais réviser une seule section. Toujours au moins deux sections différentes dans une même session de rappel, sinon on entraîne la reconnaissance du contexte (« je sais que c'est le chapitre sur TF-IDF ») au lieu de la connaissance.

---

## Difficulté pondérée

Tous les sujets ne se valent pas. Les trois points de blocage de la progression reçoivent **deux créneaux** au lieu d'un.

| Sujet | Difficulté | Créneaux |
|---|---|---|
| Levenshtein (C2) | Moyenne | J+1, J+7 |
| **Cosinus et vecteur nul (C3)** | **Élevée** | J+1, J+7, J+21 |
| **IDF et inversion de classement (C4)** | **Élevée** | J+1, J+7, J+21 |
| **Proximité ≠ synonymie (C5)** | **Élevée** | J+7, J+21 |
| Prétraitement (C1) | Moyenne | J+1, J+7 |
| Choix de représentation (C6) | Moyenne | J+21 |

**Pourquoi ces trois-là** : ce sont ceux où une conception fausse s'installe silencieusement. Un étudiant qui rate Levenshtein le sait ; un étudiant qui croit que « TF-IDF comprend le sens » ne le sait pas — il continuera à choisir TF-IDF pour des problèmes de synonymes pendant des mois.

---

## Si les délais ne sont pas tenus

Le calendrier n'est pas une prescription médicale. Trois situations et quoi faire :

- **Le J+1 est sauté.** Faire le J+7 en fusionnant les deux contenus, et décaler le J+21 à J+28. Ne pas supprimer un créneau : l'espacement a besoin d'au moins trois points.
- **Le J+1 échoue massivement** (moins de la moitié retrouvée). Ce n'est pas un problème de mémoire, c'est un problème de **première exposition** : reprendre la section concernée à froid, puis repartir sur un intervalle plus court (J+1 puis J+4 puis J+14).
- **Tout est trivial.** Allonger : J+3, J+14, J+45. Un rappel réussi sans effort ne produit plus d'effet — c'est la difficulté de récupération qui consolide, pas la réussite.

---

## Le calendrier ne s'arrête pas au cours 9

Les quatre compréhensions durables du cours 5 servent aux séances 6 à 9 **et** à la pratique professionnelle. Le dernier créneau utile se situe **deux à trois mois** après le cours : une seule tâche, le banc d'essai des quatre requêtes sur un corpus de votre travail réel. C'est à ce moment-là qu'on saura si le cours a produit une capacité ou seulement une bonne séance.
