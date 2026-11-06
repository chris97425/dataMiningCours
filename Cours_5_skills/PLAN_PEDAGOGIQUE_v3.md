# Cours 5 — Plan pédagogique v3 (conception par compétences)

**Version** : 3.0 · 2026-11-05
**Filiation** : `Cours_5/PLAN_PEDAGOGIQUE.md` v2.2 (plan du cours existant, conservé tel quel dans l'archive).
**Méthode** : UbD (`backwards-design-unit-planner`) + progression (`learning-progression-builder`) + charge cognitive (`cognitive-load-analyser`) + estompage (`worked-example-fading-designer`) + rappel (`retrieval-practice-generator`) + espacement (`spaced-practice-scheduler`) + grille (`criterion-referenced-rubric-generator`) + CFU (`k12-check-for-understanding`) + structure (`anything-to-course`).

**Ce que ce document n'est pas** : une réécriture du contenu technique. Les chiffres, les exemples et les vérifications numériques de la v2.2 sont **repris à l'identique** — ils ont été recalculés par script en novembre 2026 et sont exacts. Ce qui change, c'est la **charpente** : l'ordre, la finalité, les preuves et la charge.

---

## Étape 1 — Résultats visés (UbD Stage 1)

### Compréhensions durables

Quatre idées qui doivent survivre à l'examen, au stage, et à dans deux ans.

1. **Représenter un texte, c'est choisir ce qu'on perd.** Il n'existe pas de représentation sans perte. La question n'est jamais « quelle est la bonne représentation » mais « quelle perte ma tâche peut-elle supporter ».
2. **Pondérer est un arbitrage, pas une amélioration.** L'IDF échange de la fréquence contre du pouvoir discriminant. Il ne rapproche pas les sens.
3. **La proximité distributionnelle est une hypothèse, pas une vérité.** Deux mots proches par leurs contextes ne sont pas synonymes : `chaud` et `froid` sont voisins.
4. **Le choix de représentation se fait par la question posée**, pas par la mode. Un TF-IDF bien réglé bat un embedding mal employé.

### Questions essentielles (ouvertes, sans réponse unique)

- Pourquoi un programme qui compte les mots se trompe-t-il si souvent — et pourquoi commence-t-on quand même par là ?
- Quand un mot fréquent vaut-il moins qu'un mot rare ?
- Que faut-il qu'un nombre contienne pour qu'il porte du sens ?
- Qu'est-ce qu'on accepte de perdre, et comment le dit-on à celui qui lira le résultat ?

Ces quatre questions reviennent en S1, S5, S6 et S8. Les réponses doivent **s'approfondir**, pas se répéter.

### Connaissances et savoir-faire requis

Voir `CAPABILITIES.md` — six capacités C1 à C6. Les connaissances nommées (type, token, IDF, CBOW…) ne sont là que parce qu'une capacité en a besoin.

---

## Étape 2 — Preuves d'évaluation (UbD Stage 2 : **avant** les activités)

C'est l'inversion centrale par rapport à la v2.2. Les preuves sont définies **avant** de choisir les slides.

### Tâche de performance (transfert, non entraînée en cours)

> **Le banc d'essai des quatre requêtes**
>
> On vous donne un corpus que vous n'avez jamais vu : 40 avis clients sur des hébergements, en français, avec fautes de frappe et accents manquants. Quatre requêtes sont posées : (a) `chambre bucale` (faute), (b) `chambre calme` (employé nulle part, mais `silencieux` est utilisé partout), (c) `wifi` (fréquent, peu discriminant), (d) `vue mer` (expression).
>
> Pour chacune : choisissez une représentation parmi {comptages, TF-IDF, Word2Vec pré-entraîné, moyenne de vecteurs de mots}, justifiez par les propriétés de la requête, **prédisez l'ordre des trois premiers résultats**, puis vérifiez par le calcul. Terminez par le tableau des quatre limites que vous avez acceptées.

Pourquoi c'est une tâche de performance et pas un exercice : le corpus est nouveau, les requêtes ne portent pas le nom de la méthode, et il faut **prédire avant de calculer**. C'est C6 en situation, pas C6 récité.

### Autres preuves

| Preuve | Quand | Ce qu'elle révèle | Capacité |
|---|---|---|---|
| Diagnostic d'entrée (5 items + 1 prédiction) | S0, 3 min | Les prérequis des cours 1–4 sont-ils là ? | — (routage) |
| 6 tickets de sortie | Fin de S1 à S7 | Ce qui est retenu à chaud, et ce qui vient des sections antérieures | C1–C5 |
| 2 CFU (S2 et S5) | En séance | La conception fausse qui est en train de se former | C1, C4 |
| Exercice de clôture (3 situations) | S8 | Le transfert, à froid | C6 |
| TP 3 blocs, grille descriptive | Après la séance | Les six capacités en exécution | C1–C5 |
| `review-schedule.md` | J+1, J+7, J+21 | La rétention réelle | toutes |

### Grille de réussite (résumé — détail dans `GRILLE_TP.md`)

Quatre niveaux **qualitativement distincts**, pas quatre degrés de « bien ». Le niveau visé est **Autonome** : l'étudiant fait sans aide et nomme la limite.

---

## Étape 3 — Progression d'apprentissage

Six paliers observables, du novice à la cible. Construite avec `learning-progression-builder` (Heritage 2008, Popham 2007, Hattie & Donoghue 2016).

| Palier | Ce que l'étudiant **fait** | Rupture avec le palier précédent | Prérequis | Tâche diagnostique (2 min) |
|---|---|---|---|---|
| **1 · Découpeur** | Découpe une phrase en tokens avec `\w+` ou en coupant sur les espaces | Passe de « je lis » à « je liste » | Python, listes | `re.findall(r"\w+", "l'ordinateur")` → donner le résultat |
| **2 · Prétraiteur** | Justifie deux décisions de prétraitement et nomme une perte | Passe de « je découpe » à « je choisis » | Palier 1 | `le chat ne dort pas` → après stop words, sens conservé ? |
| **3 · Comparateur** | Calcule une distance d'édition et dit ce qu'elle ignore | Passe de « je compare des mots » à « je compare des chaînes » | Palier 2 | `chat`/`chats` : distance ? Puis `voiture`/`automobile` : distance ? |
| **4 · Vectoriseur** | Construit un vecteur de comptage et calcule un cosinus | Passe de « je compare deux mots » à « je compare deux textes » | Palier 3 + produit scalaire (cours 2) | `[1,0,1]` et `[1,1,1]` : cosinus ? |
| **5 · Pondérateur** | Calcule un IDF sklearn et **prédit** l'effet sur un classement | Passe de « je calcule » à « j'anticipe » | Palier 4 + logarithme | Un mot dans 4 documents sur 4 : IDF sklearn ? |
| **6 · Concepteur** | Choisit une représentation pour une situation neuve et nomme la limite acceptée | Passe de « j'exécute » à « je décide » | Palier 5 | Requête `voiture`, corpus dit `automobile` : quelle représentation ? |

### Dépendances

```
1 Découpeur ──▶ 2 Prétraiteur ──▶ 3 Comparateur ──▶ 4 Vectoriseur ──▶ 5 Pondérateur ──▶ 6 Concepteur
                                        │                                    │
                                        └── prérequis souple ────────────────┘
                                     (le cosinus réutilise la même idée d'angle)
```

**Prérequis durs** : 1→2→3→4→5→6. Aucun palier ne peut être sauté.
**Prérequis souples** : le cosinus (palier 4) est déjà connu du cours 2 (produit scalaire) — l'étudiant qui l'a oublié est ralenti, pas bloqué.

### Points de blocage typiques

| Entre | Ce que « bloqué » ressemble à | Cause réelle | Parade en séance |
|---|---|---|---|
| **2 → 3** | « Levenshtein mesure la ressemblance » | Confusion entre ressemblance de forme et de sens | Slide « Où ça marche, où ça casse » + exercice de transfert `voiture`/`automobile` |
| **4 → 5** | « TF-IDF trouve les documents pertinents » | Confusion entre correction de biais et compréhension | CFU 2 : quatre prédictions à trancher **avant** calcul |
| **5 → 6** | « Word2Vec comprend le sens » | Prendre une hypothèse pour un fait | Le couple `chaud`/`froid` à 0,74, montré deux fois |

**Priorité pédagogique** : le blocage 4→5 est le plus coûteux, parce qu'il produit un praticien qui croit que changer de pondération résout un problème de sens. C'est la cible de la CFU 2.

---

## Étape 4 — Analyse de charge cognitive de la version existante

Analyse menée avec `cognitive-load-analyser` (Sweller 1988/2019, Kalyuga 2003) sur les 62 slides de la v2.2.

### Verdict global

| Séquence | Charge intrinsèque | Charge extrinsèque | Diagnostic |
|---|---|---|---|
| S0 Ouverture | Faible | Faible | OK |
| S1 Difficulté | Faible | **Moyenne** | 5 exemples pour 4 causes : redondance |
| **S2 Tokens** | **Élevée** | **Élevée** | **Point chaud du cours** |
| S3 Levenshtein | Moyenne | Faible | Bien séquencé, mais **aucun estompage** |
| S4 BoW | Moyenne | Moyenne | Split-attention sur 2 slides |
| S5 TF-IDF | Moyenne | Faible | OK, mais **aucune prédiction** |
| S6 Word2Vec | Élevée | Moyenne | 9 slides, 11 notions |
| S7 Limites | Faible | Faible | OK |
| S8 Synthèse | Faible | Faible | Trop tardif pour servir |

### S2, le point chaud — chiffres

11 slides, **14 notions nouvelles** : type, token, identifiant, vocabulaire, Unicode, NFC/NFD, normalisation, tokenisation, regex, stop words, stemming, lemmatisation, POS, sous-mots.

**Interactivité des éléments** : élevée. On ne peut pas comprendre « stop words » sans avoir compris « token », ni « lemmatisation » sans « POS ». Ces notions doivent être tenues ensemble en mémoire de travail — c'est exactement le cas où la charge intrinsèque est irréductible.

**Ce qui est réductible** :

| Slide | Effet violé | Correctif appliqué en v3 |
|---|---|---|
| « Pourquoi est-ce si difficile ? » | Redondance (5 exemples pour 4 causes) | Ramené à 4 lignes, une par cause, l'exemple de la 5ᵉ ligne passe en question |
| « Normaliser, c'est choisir ce qu'on perd » | Split-attention (tableau 4 lignes + encadré Pourquoi + avertissement) | Le « Pourquoi » passe **avant** le tableau : on lit la raison, puis le tableau la vérifie |
| « Découper en tokens » | Split-attention (2 colonnes code + prose + encadré) | Deux slides distinctes : une par méthode, chacune avec son verdict |
| « Étiqueter la grammaire » | Redondance (tableau + 3 puces qui redisent le tableau) | Le tableau porte l'exemple, les puces nomment seulement l'usage |
| « Un exemple, étape par étape » | Complexité inutile (6 étapes d'un coup) | **Estompage** : 3 étapes montrées, 3 à compléter |
| « Ce qu'on range dans le dataset » | Split-attention (tableau + 3 puces + question) | La question passe en ticket de sortie |

**Effet d'inversion d'expertise (Kalyuga)** : le public a déjà `fit`/`transform` et le produit scalaire. Les rappels de cours 2 restent **une ligne**, pas un paragraphe — au-delà, ils deviennent de la redondance pour les bons et du bruit pour les autres.

### Décision structurante

S2 passe de 11 à **14 slides plus courtes**. Ce n'est pas une inflation : c'est le passage d'une slide surchargée à deux slides lisibles. Le temps total de S2 est inchangé (24 min) ; c'est la charge par slide qui baisse.

---

## Étape 5 — Séquences d'estompage

`worked-example-fading-designer` (Sweller & Cooper 1985, Renkl 2014, van Merriënboer & Kirschner 2018). **Règle** : on estompe par la fin, les dernières étapes étant les plus routinières.

### Estompage 1 — Normalisation Unicode (S2)

| Étape | Contenu | Qui fait |
|---|---|---|
| 1. Exemple complet | `"é"` → NFC (1 caractère) vs NFD (2 caractères), `a == b` faux | Le prof, slide entière |
| 2. Auto-explication | « Pourquoi `len` diffère alors que l'écran affiche pareil ? » | L'étudiant, 40 s |
| 3. Complétion | On donne `normalize("NFC", …)` sur `"été"` ; **la ligne de vérification manque** | L'étudiant écrit la vérification |
| 4. Indépendant | `"café"` copié d'un PDF : que faire, et comment le prouver ? | L'étudiant, sans notes |

**Erreur fréquente annotée** : normaliser en NFD « pour être sûr » — cela **crée** le problème au lieu de le régler.

### Estompage 2 — Matrice de Levenshtein (S3)

C'est l'estompage le plus important : la v2.2 montrait 3 slides pleines (bords, remplissage, résultat) sans jamais demander à l'étudiant de remplir une case.

| Étape | Contenu | Qui fait |
|---|---|---|
| 1. Exemple complet | `chat` / `chats` : bords + remplissage de la ligne `a` + résultat 1 | Le prof, 2 slides, **chaque case annotée du *pourquoi*** |
| 2. Auto-explication | « Pourquoi la diagonale coûte 0 ici et 1 ailleurs ? » | L'étudiant |
| 3. Complétion | Même matrice, **la dernière ligne (`t`) est vide** | L'étudiant remplit 6 cases |
| 4. Complétion avancée | `chien` / `chats` : seuls les bords sont donnés | L'étudiant fait ~80 % |
| 5. Indépendant | `ordinateur` / `ordinatuer` : matrice entière | Devoir, corrigé dans `answers/` |

**Note d'inversion d'expertise** : un étudiant qui remplit l'étape 3 sans hésiter passe directement à l'étape 5. Le prof annonce ce droit à voix haute — sinon les rapides subissent l'estompage.

### Estompage 3 — Cosinus (S4)

| Étape | Contenu | Qui fait |
|---|---|---|
| 1. Exemple complet | `le chat` vs D1 : produit scalaire 3, normes √2 et √10, cosinus 0,671 | Le prof |
| 2. Complétion | `le chat` vs D2 : le produit scalaire est donné, **les normes manquent** | L'étudiant |
| 3. Indépendant | `le chat` vs D4 : tout | L'étudiant |

**Point de vigilance** : le cosinus avec vecteur nul (`animal de compagnie`) n'est **pas** estompé — il est traité comme un cas à part entière, parce que c'est une erreur de conception (0/0), pas une étape de calcul.

---

## Étape 6 — Plan des séquences (UbD Stage 3)

**Budget** : 150 min. **Contenu** : 132 min. **Transitions, incidents, débordements** : 18 min. Les tentatives ne sont pas du temps mort : elles **sont** l'interaction, et elles sont comptées dans le contenu.

| S | Titre | Durée | Slides | Capacité | Tentative / preuve |
|---|---|---|---|---|---|
| S0 | Ouverture et contrat | 6 min | 4 | — | Diagnostic d'entrée (5 items) |
| S1 | Pourquoi le texte pose problème | 7 min | 5 | prérequis C6 | Prédiction « comment feriez-vous » |
| S2 | Du texte aux tokens | 25 min | 15 | C1 | Estompage NFC + CFU 1 |
| S3 | Distance d'édition | 18 min | 12 | C2 | Estompage matrice en 4 étapes |
| S4 | Sac de mots et cosinus | 23 min | 14 | C3 | Estompage cosinus + prédiction de classement |
| S5 | TF-IDF | 16 min | 10 | C4 | **Prédiction avant calcul** + CFU 2a/2b |
| S6 | Des mots aux vecteurs | 21 min | 10 | C5 | Calcul de paramètres à main levée |
| S7 | Limites et RAG | 10 min | 5 | C5→C6 | Ticket de sortie |
| S8 | Synthèse et transfert | 9 min | 4 | C6 | Les trois situations |
| | **Total** | **135 min** | **79** | | + 15 min de transitions et d'imprévus |

Sur 150 minutes : 135 min de contenu (tentatives comprises) + 15 min de transitions, d'incidents techniques et de débordements. Les tentatives **sont** comptées dans le contenu, pas dans la marge.

### S0 — Ouverture et contrat (6 min, 4 slides)

1. Page de titre.
2. **Diagnostic d'entrée** — 5 items courts sur les cours 1–4 (produit scalaire, normalisation, matrice de confusion, `fit`) + 1 prédiction : « à votre avis, que fait un ordinateur quand on lui demande de comparer deux phrases ? ». Réponse en `answers/`, pas sur la slide.
3. **Ce que vous saurez faire** — les six capacités, en verbes d'action, chacune rattachée à sa section. Remplace la slide d'objectifs vagues.
4. **Contrat d'apprentissage** — tentative avant explication, confiance avant vérification, ticket de sortie à chaque section, révision espacée J+1/J+7/J+21. Trois lignes. C'est ce qui distingue ce cours d'une conférence.

### S1 — Pourquoi le texte pose problème (7 min, 5 slides)

1. Deux phrases, une même scène (accroche conservée).
2. **Prédiction** : « Avant de lire la suite, écrivez en une ligne comment vous feriez » — 60 s, à voix haute dans le binôme. Aucune réponse attendue.
3. Les **quatre** sources de difficulté (ambiguïté, productivité, variabilité de surface, dépendance au contexte).
4. Quatre niveaux d'analyse (morphologique → discursif), présentés comme **niveaux**, pas comme difficultés.
5. **Ticket de sortie S1** : citer les 4 sources + 1 exemple chacune + distinguer source et niveau.

### S2 — Du texte aux tokens (24 min, 14 slides)

| # | Slide | Rôle |
|---|---|---|
| 1 | Le fil rouge : une barre de recherche | Ancre les 4 requêtes qui reviendront partout |
| 2 | Type, token, identifiant, vocabulaire | Vocabulaire minimal |
| 3 | **Prédiction** : deux « é » identiques ? | 45 s, main levée |
| 4 | Deux « é » qui ne sont pas égaux | Exemple complet |
| 5 | **Complétion** : prouver l'égalité sur `été` | Estompage 1, étape 3 |
| 6 | Normaliser, c'est choisir ce qu'on perd | Le « pourquoi » **avant** le tableau |
| 7 | **CFU 1** : quelle normalisation pour des avis clients ? | 4 options, distracteurs = fausses conceptions |
| 8 | Couper sur les espaces (et ce que ça casse) | Une méthode, son verdict |
| 9 | Garder les suites de lettres (et ce que ça casse) | L'autre méthode, son verdict |
| 10 | Stop words : ce qu'on gagne, ce qu'on risque | Le piège de la négation |
| 11 | Stemming ou lemmatisation | Tableau comparatif |
| 12 | La chaîne complète | Le pipeline en une image |
| 13 | **Complétion** : les 3 dernières étapes | Estompage sur l'exemple `Les chats d'Emily…` |
| 14 | **Ticket de sortie S2** | Mêle S1 et S2 |

Le POS tagging et les sous-mots sont **ramenés à une mention** dans la slide 12 (deux demi-lignes), pas deux slides. Le détail part en séance 6 — décision v2.2 conservée, renforcée par l'analyse de charge.

### S3 — Distance d'édition (16 min, 9 slides)

1. Deux mots se ressemblent-ils ? (retour au fil rouge `salom`)
2. Trois opérations autorisées
3. La récurrence (formule, une slide)
4. **Exemple complet, annoté** : bords de `chat`/`chats` — chaque bord justifié
5. **Exemple complet, annoté** : remplissage de la ligne `a` — la règle des trois voisines
6. **Auto-explication** : pourquoi la diagonale coûte 0 parfois, 1 ailleurs ?
7. **Complétion** : dernière ligne vide, 6 cases à remplir
8. Une distance de 1, c'est beaucoup ? (normalisation + tableau des 5 paires)
9. Où ça marche, où ça casse + **ticket de sortie S3**

`voiture`/`automobile` = 8 reste le pivot de la section : c'est le mur qui justifie tout le reste du cours.

### S4 — Sac de mots et cosinus (23 min, 12 slides)

1. Pourquoi transformer un texte en vecteur ? (maisons vs textes)
2. **Prédiction** : « le chien mord l'homme » et « l'homme mord le chien » — même vecteur ?
3. L'idée du sac de mots + les 4 documents
4. Ce que le sac garde, ce qu'il jette
5. Présence ou comptage ? (le tableau à 4 colonnes)
6. La matrice documents × termes
7. Une matrice pleine de zéros (3,7 % de non-nuls)
8. `fit` puis `transform` — et le vecteur nul
9. Mesurer un angle plutôt qu'une distance
10. **Exemple complet** : cosinus `le chat` / D1 = 0,671
11. **Complétion** : D2, puis D4 en indépendant
12. **Ticket de sortie S4** (mêle S2 et S3)

La slide « Même requête, sans les stop words » de la v2.2 est **fusionnée** dans le ticket : c'est une vérification, pas une notion.

### S5 — TF-IDF (16 min, 8 slides)

1. Tous les mots ne se valent pas (le tableau `le`/`salon`/`félin`)
2. **CFU 2a — prédiction** : requête `le chat`, TF-IDF change-t-il le classement ? Justifiez en une ligne.
3. La formule (TF × IDF, convention sklearn)
4. L'IDF sur nos quatre documents (+ la courbe)
5. **Révélation** — `le chat` : le classement **ne change pas**, les écarts se creusent
6. **CFU 2b — prédiction** : requête `félin salon`, qui gagne ?
7. **Révélation** — `félin salon` : D3 passe devant D4. Le seul cas où la pondération corrige un classement faux.
8. Ce que TF-IDF ne sait pas faire + **ticket de sortie S5**

Le couple prédiction/révélation est le cœur de la section. En v2.2, la réponse était donnée dans la même slide que la question : aucun effort de récupération.

### S6 — Des mots aux vecteurs (21 min, 10 slides)

1. Pourquoi des vecteurs de mots ? (one-hot, cosinus 0 partout)
2. L'idée de Word2Vec (Firth 1957)
3. **Auto-explication** : « dans *le ___ dort sur le canapé*, qu'est-ce qui ne peut pas aller ? »
4. La fenêtre glissante
5. CBOW et Skip-gram
6. Où sont les vecteurs (matrice `|V| × d`, formule d'agrégation)
7. **Complétion** : calculer le coût pour 10 000 mots × 100 dimensions
8. Les vecteurs du TP en 2D + le couple `chaud`/`froid`
9. Les analogies, et où elles échouent
10. **Ticket de sortie S6**

La slide « Combien de paramètres ? » de la v2.2 (prose + carte + avertissement) est **scindée** : le calcul devient une complétion, l'ordre de grandeur reste en carte.

### S7 — Limites et RAG (10 min, 5 slides)

1. Cinq limites à garder en tête (tableau conservé)
2. Un mot, plusieurs sens (`avocat`, avec les voisins réels du modèle du TP)
3. Retour au fil rouge : les six requêtes, ce qui a été réglé et ce qui reste
4. Comparer les représentations (tableau conservé — c'est la matrice de décision)
5. **Ticket de sortie S7**

### S8 — Synthèse et transfert (9 min, 4 slides)

1. La carte des capacités C1→C6, avec la question à se poser à chaque palier
2. **Exercice de transfert** : les trois situations (conservé)
3. **Le banc d'essai des quatre requêtes** — annonce de la tâche de performance, avec le corpus inédit
4. Le TP en trois blocs + le contrat de révision J+1/J+7/J+21

La slide « Ce qu'il faut retenir » en 5 puces est **supprimée** : elle arrive quand il est trop tard pour changer quoi que ce soit, et relire des puces ne produit pas de récupération.

---

## Étape 7 — Contrôle d'alignement

Vérification que les trois étages d'UbD se répondent. Une seule ligne par capacité ; toute case vide est un défaut.

| Capacité | Résultat visé (Stage 1) | Preuve (Stage 2) | Activité (Stage 3) |
|---|---|---|---|
| C1 Prétraiter | Compréhension 1 | TP bloc 1, ticket S2, CFU 1 | S2 slides 2–13 |
| C2 Levenshtein | Compréhension 1 | Exercice S3, ticket S3 | S3 slides 3–9 |
| C3 Vectoriser | Compréhensions 1 et 3 | TP bloc 2, CFU 2a, ticket S4 | S4 slides 5–12 |
| C4 Pondérer | Compréhension 2 | CFU 2b, ticket S5 | S5 slides 1–8 |
| C5 Word2Vec | Compréhension 3 | TP bloc 3, ticket S6 | S6 slides 1–10 |
| C6 Choisir | Compréhension 4 | Tâche de performance, exercice S8 | S7–S8 |

**Questions essentielles** : chacune est posée au moins deux fois, à des moments différents, avec une attente de réponse plus profonde la seconde fois.

| Question | 1ʳᵉ pose | 2ᵈᵉ pose | Ce qui doit s'approfondir |
|---|---|---|---|
| Pourquoi commencer par compter ? | S1 | S8 | De « c'est simple » à « c'est explicable et souvent suffisant » |
| Quand un mot rare vaut-il plus ? | S5 | S8 | De « quand il est rare » à « quand il discrimine, et cela dépend du corpus » |
| Que doit contenir un nombre pour porter du sens ? | S6 | S8 | De « une valeur proche » à « une position dans un espace appris » |
| Qu'accepte-t-on de perdre ? | S2 | S7 | De « les accents » à « l'ordre, le sens multiple, l'inconnu » |

---

## Étape 8 — Écart assumé avec la v2.2

| Point | v2.2 | v3 | Justification |
|---|---|---|---|
| Slides | 62 | 79 | Estompage (+9), scissions de slides surchargées (+13), prédictions (+4), tickets (+7), révélations différées (+2), moins les fusions et suppressions (−18) |
| Objectifs | 5 verbes vagues | 6 capacités observables | On ne conçoit pas de pratique pour « comprendre » |
| Preuves | définies en fin de plan | définies **avant** les activités | UbD Stage 2 |
| S2 | 11 slides, 14 notions | 14 slides plus courtes | Charge cognitive : la densité par slide baisse, le temps ne change pas |
| Levenshtein | 3 slides montrées | 5 slides dont 2 de complétion | Estompage : la v2.2 ne demandait jamais de remplir une case |
| TF-IDF | réponse et question sur la même slide | prédiction → révélation | Effort de récupération |
| Révision | absente | `review-schedule.md` J+1/J+7/J+21 | Espacement |
| Évaluation TP | absente | `GRILLE_TP.md` descriptive 4 niveaux | Critères connus avant la note |
| Synthèse | 5 puces « à retenir » | 3 situations + tâche de performance | Transfert plutôt que récitation |

**Ce qui n'a pas changé, volontairement** : les chiffres, le corpus de 4 documents, les images, le thème `neobeam`, le format 4:3, la durée, et le TP. La v2.2 est techniquement solide ; c'est sa charpente pédagogique qui manquait.
