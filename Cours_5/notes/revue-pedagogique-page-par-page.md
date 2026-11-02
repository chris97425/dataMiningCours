# Revue pédagogique page par page — Cours 5 (55 slides)

**Méthode** : 8 relecteurs indépendants, 7 à 8 pages chacun, le 2026-11-02. Consigne identique : *pour chaque page, quelle notion un étudiant de licence/master appliqué n'ayant jamais fait de NLP peut mal comprendre, et quel exemple visuel simple la débloquerait*.
**Statut** : revue de lecture seule. Les corrections objectives signalées ont été appliquées le jour même (voir §3). Le challenge Codex du PDF complet est programmé à 17:05.

---

## 1. Tableau complet

| page | titre | notion à risque | risque concret | exemple imagé proposé |
|---|---|---|---|---|
| 1 | Couverture | « RAG » jamais défini | Acronyme répété sans définition | 3 cases : question → recherche → réponse rédigée |
| 2 | Plan de la séance | TF-IDF détaché du sac de mots | Sept recettes mémorisées sans progression | Même tableau de comptes, puis pondéré |
| 3 | Deux phrases, une même scène | « mot de contenu » / « mot outil » non définis | « 0 mot commun » lu comme similarité nulle | Diagramme de Venn : 3 mots, 5 mots, 2 au centre |
| 4 | Pourquoi est-ce si difficile ? | « productivité » (sens linguistique) | Faux ami : lu comme « rendement » | Radical « google » + « -iser » → mot neuf |
| 5 | Quatre niveaux d'analyse | « discursif » vs « sémantique » | « ils » → « chats » classé au mauvais niveau | Flèche de « ils » vers « chats » par-dessus le point |
| 6 | La chaîne que nous allons construire | « vecteurs » : deux objets différents | Croit à un seul vecteur enrichi | 10 000 cases vides vs 300 cases pleines |
| 7 | De la chaîne aux tokens | token = occurrence d'une forme | Bute ensuite sur les sous-mots | Mot entier + mot coupé en deux boîtes |
| 8 | Un caractère n'est pas toujours un caractère | « caractère » = point de code ou graphème | Croit `len()` buggé | Emoji famille : 1 perçu, 5 comptés |
| 9 | Normaliser, c'est décider ce qu'on perd | `cote / côté / coté` | Croit à des variantes d'un seul mot | Trois tiroirs réétiquetés « COTE » |
| 10 | Tokeniser | `\w+` ne montre qu'un exemple | Croit l'élision gérée | Trois ciseaux ; montrer `aujourd` + `hui` |
| 11 | Les stop words | « dimensions », BoW, TF-IDF, RAG non définis | Retient « stop words = mal » | Entrepôt de 30 000 rayons, 90 % vides |
| 12 | Stemming ou lemmatisation ? | `meilleur → bon` | Généralise « lemme = synonyme » | Deux colonnes : mot déguisé vs renvoi de dictionnaire |
| 13 | Ce qu'on garde pour la suite | BPE illustré comme une analyse morphologique | Croit que BPE comprend la grammaire | BPE = zip : fusion par fréquence, pas par sens |
| 14 | Deux chaînes se ressemblent-elles ? | « distance de 8 » sans unité ni nom | Le 8 paraît arbitraire | Huit coups de crayon d'un mot à l'autre |
| 15 | Trois opérations, un coût de 1 | coût unitaire posé comme évidence | Confond distance et nombre de lettres différentes | Deux rails, colonnes alignées, un jeton par colonne |
| 16 | La récurrence | indices i/j (préfixes, 1-basés) | Écrit `a[i]` au lieu de `a[i-1]` | En-têtes de colonnes : ε, c, ch, cha, chat |
| 17 | La matrice : initialisation | lecture ε / en-têtes | Transpose lignes et colonnes | Cellule ε/ε étiquetée « chaîne vide » |
| 18 | La matrice : on remplit | min à trois voisins sur une case triviale | Ne relie pas les trois candidats | Case (t, s) : la gauche l'emporte |
| 19 | La matrice : le résultat | la matrice stocke des coûts, pas des choix | Croit que le chemin est dans la matrice | Flèches ↑ ← ↖ par case, puis fil remonté |
| 20 | Normaliser la distance | sens du score normalisé, division par zéro | Lit « 80 % similaires » à l'envers | Règle graduée 0→1, cinq paires placées |
| 21 | Où ça marche, où ça casse | O(nm) et « coûts adaptés » non définis | Conclut « inutile » au lieu de « mauvaise unité » | Jetons-lettres vs jetons-mots, distances opposées |
| 22 | L'idée du sac de mots | sac = multiensemble | Déduplique et perd `le ×2` | 3 pommes + 1 poire ≠ {pomme, poire} |
| 23 | La matrice documents × termes | ligne = point en 18 dimensions, colonnes tronquées | Recalcule sur 10 colonnes et trouve 0,75 | Wagon de 18 places, 10 vitres visibles |
| 24 | Un vecteur très creux | 0 = mot absent, pas valeur manquante | Lit les 0 comme des NaN | Façade de 50 000 fenêtres, 80 allumées |
| 25 | `fit` puis `transform` | fit imprime le formulaire, transform le remplit | Requête hors vocabulaire → vecteur nul | Formulaire à cases fixes, mot sans case |
| 26 | Similarité cosinus | angle ≠ distance ; vecteur nul | Généralise « cos 0 = rien en commun » | Flèches de longueur 1 et 10, même cap |
| 27 | Requête « le chat » | 0 = aucun mot partagé, pas « hors sujet » | Lit D3 comme non pertinent alors que c'est un synonyme | Deux flèches perpendiculaires |
| 28 | Le sac perd l'ordre | bigrammes = ordre local, pas sens | Croit les synonymes réglés | Même sac, deux phrases : qui mord qui reste invisible |
| 29 | Et si aucun mot n'est connu ? | vecteur nul, cosinus 0/0 | Confond « pas pertinent » et « aucune information » | Deux flèches de longueur zéro |
| 30 | Le comptage brut a un défaut | df vs nombre d'occurrences | Confond « 6 fois » et « 3 documents » | Deux compteurs : tours de parole vs personnes |
| 31 | Récapitulatif | — | OK | OK |
| 32 | L'idée : pondérer ce qui distingue | fréquent dans le doc vs rare dans le corpus | Lit « fréquent = important » | Mot partout = bruit de fond ; mot rare = balise |
| 33 | Les deux facteurs | log, lissage +1, normalisation L2 | Voit ln comme une formule magique | Barres 1/4/100 docs : 1,9 → 1,2 → 1,0 |
| 34 | Calcul sur notre corpus | IDF plancher à 1, jamais zéro | Attend 0 pour « le » | Jauge dont la barre de « le » reste visible |
| 35 | Requête « le chat » en TF-IDF | « accentue les différences » alors que tout baisse | Croit que TF-IDF augmente les scores | Élastique : tout rétrécit, l'écart se creuse |
| 36 | Le cas où le classement bascule | colonne « Comptages » remplie de décimaux | 0,224 lu comme un nombre d'occurrences | Balance : « salon » s'allège, « félin » s'alourdit |
| 37 | Les limites de TF-IDF | cos(voiture, automobile) = 0 | Lu comme « opposés » | Deux flèches à angle droit : aucun axe commun |
| 38 | Récapitulatif | IDF = 1 lu comme un poids fort | Confond plancher et sommet | Jauge dont 1 est le bas de l'échelle |
| 39 | Un one-hot ne dit rien | orthogonalité ; glose de Firth | Confond « apparaissent ensemble » et « mêmes contextes » | Test à trous : « le ___ dort » accepte chat, refuse canapé |
| 40 | La fenêtre glissante | k = largeur totale ou rayon ? | Rate les bornes | Cache de 5 cases glissé, case centrale colorée |
| 41 | CBOW et Skip-gram | sens des flèches ; « la même chose » | Entrée et sortie inversées | 4 flèches convergent vs 4 qui rayonnent |
| 42 | Où sont les vecteurs ? | `e_w`, `h` non définis ; `\|C\| ≤ 2k` | Cherche les vecteurs dans la couche cachée | Tableur : lignes = mots, colonnes = dimensions |
| 43 | Combien ça coûte ? | paramètres ≠ calcul | Confond 60 M de poids et \|V\| scores par paire | Deux compteurs : mémoire fixe, calcul à chaque paire |
| 44 | Ce que ça donne | similarité distributionnelle ≠ sens | Repart en croyant que le modèle comprend | Curseur chaud–froid : opposés sur l'axe, voisins sur la carte |
| 45 | Lire un espace d'embeddings | la différence est une direction, pas un mot | Croit l'égalité exacte et démontrée | Autocollant « féminin » décollé puis recollé |
| 46 | Ce que ça vaut vraiment | lire un cosinus de 0,37 | Y voit 37 % de réussite | Rapporteur : 0,37 = 68° |
| 47 | D'un mot à un document | le pooling est un sac de mots | Croit que moyenner donne le sens d'une phrase | « Le chat mange la souris » et son inverse |
| 48 | Cinq limites | la ligne « Lexical » contredit la p. 44 | Lit voiture/automobile = 0 partout | Deux colonnes : one-hot 0, Word2Vec proches |
| 49 | Un vecteur par contexte | un vecteur par occurrence, pas par sens | Croit à deux vecteurs stockés | Empreinte digitale : jamais la même, toujours reconnaissable |
| 50 | RAG phase 1 | « hors ligne », « chunk », « encodeur » | « hors ligne » lu comme « sans Internet » | Catalogue imprimé avant l'ouverture |
| 51 | RAG phase 2 | « top-k », « prompt », retriever vs LLM | Croit que le LLM fouille la base | Bibliothécaire qui apporte k photocopies |
| 52 | Qui traite quoi | `rappel@k`, HNSW, « fidélité » | Acronymes pris pour des produits | Filet de k mailles ; plan de métro |
| 53 | La carte du cours | « jette » de l'information | Lu comme un défaut à corriger | Presse-fruits : on garde le jus, on jette la pulpe |
| 54 | Trois situations | situation 2 : avocat | Répond « Word2Vec » alors qu'il moyenne les sens | Une photo moyenne de deux visages |
| 55 | Le TP | vecteur nul, fit/transform, budget | 47 min annoncées pour 60 | Frise de 60 min, dernière case « marge » |

---

## 2. Les six pages les plus à risque

1. **p. 42 — `e_w`, `h`, `|C| ≤ 2k`** : trois symboles non définis dans la même formule. C'est la page qui perd les étudiants.
2. **p. 36 — colonne « Comptages » en décimales** : fausse la lecture de tout le comparatif comptages / TF-IDF.
3. **p. 18 — case de la matrice** : le calcul affiché ne correspondait pas à la matrice.
4. **p. 48 — « Lexical : cosinus 0 »** : contredit la p. 44 où Word2Vec rapproche `voiture` et `automobile`.
5. **p. 33 — log + lissage + L2** : trois notions pour une seule formule, sans image.
6. **p. 50 — numérotation S6 / séance 7** : deux systèmes de numérotation dans la même phrase.

---

## 3. Corrections appliquées le 2026-11-02

| Page | Correction |
|---|---|
| 18 | `gauche = 2+1 = 3` → `gauche = 1+1 = 2` (la case de gauche vaut 1, pas 2) |
| 36 | colonne « Comptages » → « Cosinus (comptages) » / « Cosinus (TF-IDF) » |
| 38 | « un mot présent partout garde un IDF de 1 » + « un **plancher**, pas un poids fort » |
| 42 | définition de `e_w`, `h`, et origine du `≤` (fenêtre tronquée au premier mot) |
| 48 | ligne « Lexical » → « **Lexical** (BoW, TF-IDF) » |
| 50 | `(S6)` / `(S4)` → « séance 5, section 6 » / « section 4 » |
| 55 | ajout : « 47 min de blocs + **13 min** de consignes, erreurs et questions » |
| 2 | glose du sigle RAG (il apparaît dès la couverture) |
| 3 | définition de « mot de contenu » |

---

## 4. Risques signalés mais NON corrigés (à arbitrer)

- **p. 8 vs p. 9** : la p. 8 donne `normalize("NFC")` comme règle pratique, la p. 9 prévient que refaire la normalisation peut contredire le tokenizer. Il faudrait une phrase d'arbitrage explicite : comparer des chaînes brutes → NFC ; passer à un tokenizer préentraîné → ne rien faire.
- **« token » change de sens** (mot en p. 7 et 10, sous-mot en p. 13) sans avertissement.
- **p. 46** : comparer un cosinus de vecteurs-différence (0,37) à des cosinus de voisins (0,6–0,9) mélange deux échelles.
- **p. 49** « vecteur A / vecteur B » suggère un catalogue fini de sens, alors que le vecteur est recalculé à chaque occurrence.
- **p. 50** : « encodeur » pourrait être glosé en une ligne (« il ne chiffre rien, il traduit en coordonnées »).
