# Cours 5 — Fondamentaux du NLP et préparation au RAG

**Plan pédagogique — v2.2 (validé, décisions utilisateur intégrées, aligné sur le cours produit)**

| | |
|---|---|
| Formation | Data Mining — cours 5 (suite des cours 1 à 4) |
| Durée | 3 h 30 = 2 h 30 théorie + 1 h TP |
| Public | Étudiants ayant suivi les cours 1–4 (data mining appliqué, Python/scikit-learn) |
| Auteur | Christopher de Boisvilliers |
| Statut | **Plan validé le 2026-11-02.** Slides (56) et TP produits ; contrôle de cohérence finale en cours |
| Revue externe | Codex / `gpt-5.6-sol`, raisonnement `xhigh`, 2026-11-02 — verdict v1 : **À RESTRUCTURER** (rapport intégral : `Cours_5/notes/revue-codex-v1.md`) |

**Décisions utilisateur du 2026-11-02** : **58 slides à la livraison** (54 au moment de la validation, puis « Le sac, mécaniquement », « Remplir les cases : présence ou comptage ? » et « Objectifs de la séance ») · POS tagging à 3 lignes dans le pipeline · **construction pas à pas de la matrice de Levenshtein dans le tronc (+4 min sur S3)** · embeddings du TP pré-calculés et commités.

**Ce qui change entre v1 et v2** : 73 → 54 slides ; 145 → 120 minutes de contenu avec 30 minutes explicitement réservées à l'interaction ; corpus d'exemple unique de 4 documents recalculé avec la convention scikit-learn ; schéma RAG séparé en indexation hors ligne / interrogation en ligne ; TP ramené à 3 blocs avec dépendances préinstallées ; suppression de la formule softmax de Word2Vec ; correction des exemples fautifs signalés par la revue.

**Ce qui change entre v2.1 et v2.2** : 54 → 58 slides (les chiffres du §4 sont désormais ceux du fichier `presentation.md` réel) ; slide d'objectifs ajoutée en S0 ; deux slides de clarification sur la mécanique du sac de mots en S4 ; correction de la valeur `félin` du tableau S4 (0,333 et non 0,378) ; bloc 1 du TP à 4 questions ; accroche des deux phrases rattachée à S1 dans le plan ; titres de bandeau harmonisés avec le plan de la séance ; entrée « Les 5 séances » renommée « du texte aux vecteurs ».

---

## 1. Audit de l'existant

### 1.1 Les quatre cours

| Cours | Sujet | Fichier de slides | Pages PDF | TP |
|---|---|---|---|---|
| Cours_1 | Clustering, K-means, KNN, distances | *(pas de `presentation.md` : `cours1.pdf`)* | — | `TP1/Cours2.ipynb` + dataset `Links/` (≈10 000 `.txt`) |
| Cours_2 | Régression linéaire, moindres carrés, descente de gradient, SGD | `Cours_2/presentation.md` | 65 | `TP2/Tp2.ipynb` |
| Cours_3 | Statistiques : loi normale, TCL, p-value, tests d'hypothèse | `Cours_3/presentation.md` | 81 | — |
| Cours_4 | Fonctions de perte, régression logistique, scoring (matrice de confusion, accuracy, recall, precision, F1) | `Cours_4/presentation.md` | 45 | `tp/tp4.pdf` |

**Niveau réellement installé à l'entrée du cours 5** (vérifié dans les fichiers, pas supposé) :

- Python + scikit-learn, pipelines `fit`/`predict` (cours 2), `train_test_split`, standardisation.
- Produit scalaire et vecteur de paramètres, descente de gradient, SGD, notion de fonction de perte (cours 2).
- Statistiques : loi normale, TCL, p-value, intervalle de confiance (cours 3).
- Score linéaire $\beta^\top x$, sigmoïde, entropie croisée binaire, matrice de confusion, accuracy / recall / precision / F1 (cours 4).
- **Non installé** : couche de neurones, projection matricielle, softmax, padding, notion de token. Le cours 4 s'arrête à la régression logistique — c'est la contrainte principale de conception.

### 1.2 Conventions techniques constatées

- **Front-matter MARP** identique dans les cours 2, 3, 4 :

  ```yaml
  marp: true
  theme: neobeam
  paginate: true
  size: 4:3
  math: mathjax
  header: Cours Esiroi 2025
  footer: Data mining - Christopher de Boisvilliers
  ```

  Le cours 5 conserve la structure mais s'écarte sur trois points assumés : `header: Cours Esiroi 2026` (année de l'édition), `html: true` (indispensable pour les `<div>` de mise en page) et un `title` réel au lieu du `title: Marp custom themes` resté par défaut dans les cours 3 et 4. Le bloc `style:` des cours 3 et 4 (`pre, code { font-size: 100px !important }`) n'a pas été repris : c'est un reliquat de test.

- **Thème** : `themes/neobeam.css` (556 lignes, dérivé de *Beam*). Copie locale par cours. `Cours_3` et `Cours_4` partagent exactement le même fichier (md5 `83e636c3…`) → version de référence à reprendre.
- **Hiérarchie** : `#` pour le titre et le plan, `###` en gras pour le titre de slide, `##` rare.
- **Navigation** : `<!-- _class: title -->` pour la page de titre, `<!-- header: … -->` pour changer le bandeau à chaque section, `---` entre slides.
- **Images** : `images/` local, `![width:400px](./images/x.png)`, `<div style="display:flex">` pour les paires. GIF acceptés (`Cours_2/images/*.gif`).
- **Style** : question directe à la classe, exemple chiffré avant la formule, rappel explicite des cours précédents.
- **Dossiers annexes** : `notes/` (compléments mathématiques), `tp/`, `themes/`. Export `presentation.pdf` commité à côté du `.md`.

### 1.3 Capacités MARP réellement vérifiées

Test effectué avec `@marp-team/marp-cli v4.5.1` (marp-core 4.4.0) et le thème `neobeam.css` du cours 4 :

| Fonction | Statut | Preuve |
|---|---|---|
| Formules LaTeX (`math: mathjax`) | ✅ | PDF de test, formule cosinus rendue correctement |
| Puces progressives (`*` fragments) | ✅ en HTML — figées sur une slide en PDF | `data-marpit-fragments="3"` dans l'export HTML |
| Images locales | ✅ avec `--allow-local-files` | avertissement CLI sinon |
| SVG vectoriels, `<div>` + `style` inline | ✅ | slide de test |
| GIF animés | ✅ (déjà utilisés au cours 2) | `images/*.gif` |
| Animations CSS temporelles | ❌ non fiables en PDF (rendu statique) | — |
| Classe de slide spéciale | `section.title` uniquement | `grep '^section\.'` sur le thème |
| Police / couleurs | Roboto, Roboto Mono, Noto Sans Math ; `--primary #3d65f6` | `:root` du thème |
| Surface utile | 960 × 720 px (4:3) → ~55 lignes, tableaux ≤ 5 colonnes | test de rendu |

**Conséquence** : tout mécanisme progressif (matrice de Levenshtein, fenêtre glissante, construction du BoW) sera rendu par une **séquence de slides montrant les étapes**, jamais par une animation.

### 1.4 Lacunes pédagogiques relevées

1. **Aucun cours n'introduit la notion de représentation vectorielle d'un texte** — le cours 4 s'arrête aux métriques. La marche vers les embeddings serait vertigineuse sans ce cours 5.
2. **Pas de schéma de pipeline en ouverture** : les cours 2 à 4 entrent directement dans la formule.
3. **Coquilles présentes** dans les cours 3 et 4 (`Reccal`, `régresion`, `Intérpretation`) — à ne pas reproduire.
4. **Slides parfois surchargées** (cours 3 : tableaux de 6 lignes + paragraphe) — le 4:3 pardonne peu.

---

## 2. Références et convergence pédagogique

| Source | Ordre des notions | Ce qu'on retient |
|---|---|---|
| **Jurafsky & Martin**, *Speech and Language Processing*, 3ᵉ éd. (draft 2026) | 1 Introduction → 2 **Words and Tokens** (regex, normalisation, **edit distance**) → 3 N-gram LMs → 4 Régression logistique / Naive Bayes → 5 **Embeddings** → 6 Réseaux de neurones → 7 Transformers | L'édition de distance est enseignée **immédiatement après** la tokenisation, avant toute vectorisation |
| **CMU 11-411** (E. Nyberg) | Paysage NLP → Words & Tokens → N-gram → Naive Bayes → Régression logistique → **Embeddings** → … → **IR & RAG** | Le parcours se termine par IR/RAG : notre série vise la même cible |
| **CentraleSupélec, CM1** (J. Legrand, 2023) | Intro → *Why NLP is hard* → niveaux d'analyse → représentations de documents (BoW, TF-IDF, cosinus) → représentations de mots (one-hot, LSA/SVD) | Structure de référence des deux premiers blocs et du couple BoW/TF-IDF |
| **Stanford CS224N** | Ouvre sur les *word vectors* | Public ML/DL avancé : non transposable ici |
| **Le Wagon, `06-DL_05-NLP`** (support fourni) | Ouvre sur les RNN, puis tokenisation → embeddings → Word2Vec/Gensim | Divergent sur l'ordre, mais excellente intuition « token entier ≠ solution » |

**Convergence partielle, pas unanimité** : les trois références classiques (Jurafsky, CMU, CentraleSupélec) suivent `tokens → distance d'édition → sac de mots → TF-IDF + cosinus → embeddings`. CS224N et Le Wagon font d'autres choix, assumés. L'ordre retenu ici suit les trois premières, pour deux raisons liées à ce public précis :

1. **Un bloc d'ouverture « pourquoi le langage est difficile »** (8 min) plutôt qu'une entrée par les formules : le public est data-mining appliqué, pas linguistique, et le besoin doit précéder l'outil.
2. **Word2Vec en fin de cours** et non en ouverture : CS224N peut ouvrir dessus parce que son public maîtrise les gradients ; ici, la projection matricielle doit être introduite explicitement (elle ne l'a jamais été au cours 4).

---

## 3. Arbitrages sur les 18 objectifs demandés

| # | Notion demandée | Décision | Justification | Où |
|---|---|---|---|---|
| 1 | Pourquoi le langage est difficile | **Gardé** | Crée le besoin, coût faible | S1 |
| 2 | Texte brut → données exploitables | **Gardé** | Fil conducteur | S2 |
| 3 | Tokenisation | **Gardé, recentré** | Cœur du sujet ; sous-mots en teaser seulement | S2 |
| 4 | Stop words | **Gardé, 1 slide** | Utile mais piège (négation, RAG) | S2 |
| 5 | Normalisation, stemming, lemmatisation | **Gardé** | Fort rendement pratique, présenté comme *décisions*, pas comme recette | S2 |
| 6 | POS tagging | **Réduit à 3 lignes** | Outil de pipeline ; le détail part au cours 6 | S2 |
| 7 | Similarité entre chaînes | **Fusionné avec 8** | Levenshtein *est* la réponse | S3 |
| 8 | Distance de Levenshtein | **Gardé, allégé** | Intuition + matrice résultat ; construction pas à pas en annexe | S3 |
| 9 | Bag of Words | **Gardé, noyau du cours** | Base du reste | S4 |
| 10 | TF-IDF | **Gardé** | Meilleur rapport valeur/coût | S5 |
| 11 | Mots → vecteurs | **Gardé** | Charnière | S6 |
| 12 | Word2Vec | **Gardé, sans dérivation** | Intuition CBOW/Skip-gram ; pas de softmax | S6 |
| 13 | Proximité entre vecteurs | **Gardé** | Réutilise le cosinus | S4 + S6 |
| 14 | Similarité cosinus | **Gardé** | Formule unique réutilisée 3 fois | S4 |
| 15 | Arithmétique vectorielle | **Gardé avec mise en garde** | Mémorable, mais il faut dire où ça échoue | S6 |
| 16 | Limites des classiques | **Gardé** | Moteur de la progression, dit section par section | S3–S7 |
| 17 | Représentations contextuelles / Transformers | **Réduit à 1 slide d'intuition** | Le cours 6 les traite ; ici on crée le manque | S7 |
| 18 | Préparation au RAG | **Gardé, fil rouge** | Annoncé en S0, construit en S7 | S0 + S7 |

### Ajouts nécessaires (absents de la liste)

| Ajout | Pourquoi |
|---|---|
| **A. Type, token, identifiant, vocabulaire** | Vocabulaire de base sans lequel « tokenisation » reste flou |
| **B. `fit` / `transform`** | Le mécanisme qui explique pourquoi une requête inconnue donne un vecteur nul |
| **C. OOV et vecteur nul** | L'échec le plus fréquent en production, et le pont vers les sous-mots |
| **D. N-grammes (bigrammes)** | Seule parade simple à la perte d'ordre du BoW |
| **E. Hypothèse distributionnelle** (Firth, 1957) | Sans elle, Word2Vec est un tour de magie |
| **F. Embedding de mot vs embedding de phrase** (et le *pooling*) | **Le** maillon manquant vers le RAG : un chunk n'est pas un mot |
| **G. Séparation indexation / interrogation** | Structure réelle de tout système RAG |

### Reporté explicitement

- Détails octets / points de code et panorama NFC/NFD → une démonstration de 30 s suffit ici.
- POS tagging détaillé, jeux d'étiquettes, préparation à la NER → cours 6.
- Construction complète de la matrice de Levenshtein, complexité, Jaccard → annexe + exercice optionnel du TP.
- Comparaison de plusieurs stemmers/lemmatiseurs → hors cours.
- Softmax, negative sampling, dérivation Word2Vec, GloVe, fastText → cours 6.
- Historique ELMo/BERT et mécanisme d'attention → cours 6.
- `rappel@k`, MRR, protocole d'évaluation → cours 7.
- Analyse détaillée des biais → cours 6 et 9 (une alerte d'une phrase reste ici).

---

## 4. Plan détaillé — 2 h 30 de théorie

**Budget** : **122 minutes de contenu + 28 minutes explicitement réservées** aux questions, aux deux démonstrations live, aux transitions et aux incidents techniques = 150 minutes. Ces 28 minutes ne sont pas « la marge » : elles sont réparties mentalement sur chaque séquence et doivent être consommées par l'interaction. (Les deux slides ajoutées en S4 ont pris 2 minutes sur cette réserve.)

**Volume cible** : 59 slides (mécanique du sac de mots + POS tagging).

### S0 — Ouverture (3 min, 3 slides)

- **Objectif** : poser le problème et situer le cours dans les 5 séances.
- **Notions** : corpus, token, représentation, retrieval.
- **Contenu réel** : page de titre + plan de la séance (7 sections, frise des séances 5 à 9, glose du sigle RAG) + **slide d'objectifs** : 5 objectifs en verbes d'action, chacun rattaché à sa section, puis les prérequis (cours 1 à 4, aucune connaissance en linguistique supposée). Cette slide reprend l'usage du cours 4 (« Objectifs du début de cours »).
- **Formules** : aucune. **Transition** : l'accroche des deux phrases ouvre S1 — pourquoi est-ce si difficile ?
- **Acquis** : savoir où l'on va, et que ce cours précède une série de 4 séances sur les embeddings, la recherche vectorielle et le RAG.

### S1 — Pourquoi le langage est difficile (7 min, 4 slides)

- **Objectif** : identifier **quatre** sources de difficulté (liste close), puis distinguer cette liste des *niveaux d'analyse*, qui est une autre classification.
- **Les quatre sources** : (1) ambiguïté, (2) productivité / créativité, (3) variabilité de surface, (4) dépendance au contexte.
- **Accroche (slide 1 de S1, corrigée)** : « Le chat dort sur le canapé. » / « Un félin se repose sur le sofa. » — 13 occurrences, **10 formes**, **2 formes communes** (`le`, `sur`), **0 mot de contenu commun**. Toute méthode lexicale des cours 1–4 conclut « rien à voir ». Définition de « mot de contenu » affichée sur la slide.
- **Exemples** : `avocat` (fruit / métier) ; `J'ai vu l'homme avec le télescope` ; `C'est chanmé` (argot hors vocabulaire) ; `La banque était fermée` (indécidable sans contexte).
- **Illustration** : schéma des niveaux d'analyse (morphologique → syntaxique → sémantique → discursif), présenté comme **niveaux**, pas comme difficultés.
- **Transition** : pour traiter tout ça, il faut d'abord découper.
- **Acquis** : citer 4 causes de difficulté, 1 exemple chacune, et ne pas les confondre avec les niveaux d'analyse.

### S2 — Du texte aux tokens (19 min, 8 slides)

- **Objectif** : construire une chaîne de prétraitement **minimale et justifiée**, en sachant à chaque étape ce qu'on perd.
- **Notions** : type / token / identifiant / vocabulaire ; normalisation Unicode ; tokenisation ; stop words ; stemming vs lemmatisation ; mention de POS et de sous-mots.
- **Prérequis** : S1.
- **Déroulé** :
  1. Pipeline en 5 étapes + définitions (type, token, id, vocabulaire).
  2. Unicode : `len("é") == 1` (NFC) mais `len(unicodedata.normalize("NFD","é")) == 2` — démonstration live, 1 slide, pas de théorie des encodages.
  3. Normalisation : tableau *décision → quand la prendre → ce qu'on perd* (minuscules, accents, ponctuation, chiffres, espaces).
  4. Tokenisation : espaces (échec sur `l'ordinateur`, `aujourd'hui`), `\w+` (gère `cœur`, `été`, mais coupe les élisions), ponctuation. Constat : aucun découpage naïf ne suffit en français.
  5. Stop words : gain de dimension, **piège** (`je ne veux pas` → `veux`), et pourquoi on ne les retire **pas** pour un Transformer ou un RAG.
  6. Stemming vs lemmatisation : tableau (`mangeons / mangera / mangé / mangeais` → `mang` vs `manger`), coût, dépendance au POS.
  7. Sortie de séquence : ce qu'on garde (sous-mots = réponse aux mots inconnus, cours 6 ; POS = outil, pas concept).
- **Illustrations** : pipeline vertical SVG ; slide avant/après avec tokens supprimés ; tableau stemming vs lemme.
- **Formules** : aucune. Une regex en bloc code.
- **Démo live** : `re.findall(r"\w+", phrase)` sur une phrase réelle (30 s).
- **Transition** : on a des tokens propres ; comment dire que deux textes se ressemblent ?
- **Acquis** : normaliser, tokeniser, choisir ses stop words, distinguer radical et lemme, et **savoir que chaque choix dépend de la tâche**.

### S3 — Distance d'édition (15 min, 8 slides)

- **Objectif** : mesurer une similarité au niveau des caractères, puis montrer que ça ne dit rien du sens.
- **Notions** : Levenshtein (insertion, suppression, substitution) ; conditions initiales ; normalisation de la distance ; Damerau (transposition).
- **Exemples vérifiés** :

  | Paire | Distance | `1 − d/max(len)` |
  |---|---|---|
  | `chats` / `chat` | 1 | 0,80 |
  | `carton` / `cartons` | 1 | 0,86 |
  | `chien` / `chats` | 3 | 0,40 |
  | `ordinateur` / `ordinatuer` | 2 (1 en Damerau) | 0,80 |
  | `voiture` / `automobile` | 8 | 0,20 ← **le mur** |

- **Illustrations** : récurrence complète (avec `lev(i,0)=i`, `lev(0,j)=j`) ; puis **construction pas à pas de la matrice `chat → chats` en 3 slides** (initialisation de la première ligne et de la première colonne / remplissage des lignes 2 et 3 / remplissage final + chemin optimal). Chaque slide surligne la case calculée et les trois cases candidates.
- **Formule** :

  $$\text{lev}(i,j)=\min\big(\text{lev}(i-1,j)+1,\ \text{lev}(i,j-1)+1,\ \text{lev}(i-1,j-1)+[a_i\neq b_j]\big),\quad \text{lev}(i,0)=i,\ \text{lev}(0,j)=j$$

  La normalisation `1 − d/max(len)` est présentée comme **une convention parmi d'autres**, pas comme « la » similarité.
- **Transition** : `voiture` et `automobile` sont à distance 8. Il faut changer d'unité : comparer des mots.
- **Acquis** : interpréter une distance, savoir qu'elle ne capture pas le sens, connaître son usage réel (correcteur, dédoublonnage).
- **Décision utilisateur** : la construction pas à pas reste **dans le tronc** (+4 min), et non en annexe. L'exercice optionnel du TP (implémentation complète en Python) est conservé pour les plus rapides.

### S4 — Sac de mots et cosinus (24 min, 12 slides)

- **Objectif** : représenter un document par un vecteur et classer des documents par similarité.
- **Corpus de référence unique** (utilisé aussi en S5) :

  ```
  D1  le chat dort sur le canapé du salon
  D2  le chien dort sur le tapis du salon
  D3  un félin se repose sur un sofa
  D4  le salon est grand et le salon est clair
  ```

  Vocabulaire : **18 termes**. Matrice 4 × 18.

- **Notions** : vocabulaire, matrice documents × termes, vecteur creux, `fit`/`transform`, norme L2, cosinus, classement, perte d'ordre, bigrammes, OOV.
- **Résultats vérifiés** (scikit-learn) :

  | Requête | D1 | D2 | D3 | D4 |
  |---|---|---|---|---|
  | `le chat` (comptages) | **0,671** | 0,447 | 0 | 0,365 |
  | `le chat` (TF-IDF) | **0,641** | 0,288 | 0 | 0,214 |
  | `animal de compagnie` | 0 | 0 | 0 | 0 |
  | `félin` (comptages) | 0 | 0 | **0,333** | 0 |
  | `félin salon` (comptages) | 0,224 | 0,224 | 0,236 | **0,365** |
  | `félin salon` (TF-IDF) | 0,144 | 0,144 | **0,291** | 0,214 |

- **Points de méthode** :
  - `fit` sur le corpus puis `transform` sur la requête : le vocabulaire est **figé** à l'entraînement.
  - Une requête dont **aucun** mot n'est au vocabulaire donne un **vecteur nul** → cosinus 0 partout (et mathématiquement 0/0). C'est l'échec le plus fréquent en production.
  - Le cosinus mesure un angle, pas une longueur : un document long n'est pas avantagé.
- **Illustrations** : heatmap de la matrice ; deux vecteurs, leur angle et la comparaison avec la distance euclidienne sur **une seule slide** ; slide « même sac, sens inverse » (`le chien mord l'homme` / `l'homme mord le chien`).
- **Formule** :

  $$\cos(\theta)=\frac{\mathbf a\cdot\mathbf b}{\|\mathbf a\|\,\|\mathbf b\|}=\frac{\sum_i a_ib_i}{\sqrt{\sum_i a_i^2}\,\sqrt{\sum_i b_i^2}}$$

- **Transition** : les poids sont des comptages bruts — `le` pèse autant que `rag`.
- **Acquis** : construire un BoW, calculer un cosinus, classer, expliquer perte d'ordre, OOV et vecteur nul.
- **Point de vigilance pédagogique** : ne pas affirmer qu'un classement « devrait » être différent. La méthode lexicale se trompe **par absence de terme**, pas par mauvais ordre — c'est ce que montre `animal de compagnie`.

### S5 — TF-IDF (15 min, 7 slides)

- **Objectif** : pondérer les termes selon leur pouvoir discriminant, et savoir quand cela change réellement un classement.
- **Convention unique retenue** : celle de **scikit-learn**, puisque c'est elle que le TP utilise.

  $$\text{idf}(t)=\ln\!\left(\frac{1+N}{1+\text{df}(t)}\right)+1,\qquad w_{t,d}=\text{tf}(t,d)\times\text{idf}(t),\qquad \text{puis normalisation } L_2$$

  Le TF est le **comptage brut** (pas la fréquence relative) : c'est le comportement par défaut de `TfidfVectorizer`.
- **Exemples vérifiés** (4 documents, donc `N = 4`) : `idf(chat) = ln(5/2)+1 = 1,916` ; `idf(le) = ln(5/4)+1 = 1,223` ; `idf(dort) = ln(5/3)+1 = 1,511`. Un mot présent partout (`le`, `sur`, `salon`) ne descend pas à 0 mais à 1,0–1,2 : le lissage sklearn **ne supprime jamais** complètement un terme.
- **Résultat honnête** : sur `le chat`, l'ordre **ne change pas** (D1 reste premier), mais l'écart se creuse (D2 : 0,447 → 0,288).
- **Le cas où ça change vraiment** : requête `félin salon`.
  - comptages : D1 0,224 · D2 0,224 · D3 0,236 · **D4 0,365** → D4 gagne parce qu'il répète `salon`
  - TF-IDF : D1 0,144 · D2 0,144 · **D3 0,291** · D4 0,214 → D3 gagne, `salon` étant banalisé
  - C'est **le** moment pédagogique de la séquence : la pondération corrige un classement réellement faux.
- **Limites** : synonymes (`voiture`/`automobile` → 0), polysémie, ordre, dépendance au corpus (l'IDF change si le corpus change).
- **Transition** : aucune dimension commune entre `voiture` et `automobile` → il faut des vecteurs denses.
- **Acquis** : calculer un IDF avec la convention sklearn, expliquer le rôle du log et du lissage, prédire quand TF-IDF change un classement.

### S6 — Des mots aux vecteurs : Word2Vec (22 min, 9 slides)

- **Objectif** : comprendre comment on fabrique des vecteurs qui rapprochent les mots de contextes similaires.
- **Notions** : one-hot et orthogonalité ; hypothèse distributionnelle ; fenêtre de contexte ; CBOW / Skip-gram ; matrice de projection ; agrégation du contexte ; coût en paramètres ; voisins ; analogies ; limites.
- **Prérequis réels** : cosinus (S4) ; produit scalaire et vecteur de paramètres (cours 2). **Pas** de softmax, **pas** de couche de neurones : la projection est introduite ici comme « une matrice de poids qu'on ajuste », sans formalisme de réseau.
- **Exemples vérifiés** :
  - One-hot : deux mots distincts ont un cosinus **exactement nul**. `chat` et `chien` sont aussi éloignés que `chat` et `pneu`.
  - Fenêtre glissante, `le(0) chat(1) dort(2) sur(3) canapé(4)`, fenêtre = 2 : pour la cible `dort` (indice 2), le contexte est `le(0)`, `chat(1)`, `sur(3)`, `canapé(4)` — écart maximal 2, donc bien dans la fenêtre. (À écrire avec les indices sur la slide pour lever toute ambiguïté.)
  - Coût : table d'entrée `|V| × d` **plus** table de sortie `|V| × d` → 10 000 mots × 100 dimensions ≈ **2 × 10⁶ poids**, pas 10⁶.
- **Formule unique** (agrégation seulement) :

  $$h=\frac{1}{|C|}\sum_{w\in C}e_w \qquad \text{avec } C=\text{contexte}\setminus\{w_t\},\ |C|=2k$$

  Puis, **en mots** : « on calcule un score pour chaque mot du vocabulaire, transformé en probabilité ; l'entraînement ajuste les deux matrices pour augmenter la probabilité des mots réellement observés ». Mention écrite : *softmax et negative sampling → cours 6*.
- **Ce que produit Word2Vec** : une similarité **distributionnelle**, pas « le sens ». Deux mots peuvent être proches parce qu'ils partagent des contextes (antonymes, co-hyponymes) — c'est une force et un piège.
- **Analogies** : `roi − homme + femme ≈ reine`, interprétation comme translation, et **quand ça échoue** (rare, dépend du corpus, biais).
- **Limites annoncées** : un mot = un seul vecteur (polysémie), ordre ignoré, OOV, biais de corpus.
- **Le maillon vers le RAG** : un document ou un chunk n'est **pas** un mot. Il faut agréger (*pooling*) ou entraîner un encodeur de phrases — ce que fait `sentence-transformers` (cours 6). Sans ce maillon, le RAG paraît magique.
- **Illustrations** : one-hot creux vs vecteur dense **sur la même slide que l'hypothèse distributionnelle** ; CBOW et Skip-gram côte à côte ; fenêtre glissante en 2 slides ; nuage 2D de 20 mots français ; triangle `roi/homme/femme/reine` **sur la slide des limites**.
- **Acquis** : expliquer l'hypothèse distributionnelle, distinguer CBOW et Skip-gram, justifier la dimension `d`, lire une similarité, nommer 4 limites.

### S7 — Limites, contexte, et ce qu'il faut pour un RAG (11 min, 5 slides)

- **Objectif** : nommer les limites, entrevoir la réponse contextuelle, et décrire le pipeline RAG complet.
- **Exemples** : `avocat` (fruit / métier), `glace` (dessert / miroir / glace d'eau), `vol` (avion / délit) → un seul vecteur pour plusieurs sens.
- **Slide 1 — récapitulatif des limites** : lexical (S4/S5), statique (S6), ordre, OOV, biais.
- **Slide 2 — embeddings contextuels** : le vecteur d'un mot dépend de la phrase. Une seule slide d'intuition, sans historique ELMo/BERT et sans attention (cours 6).
- **Slide 3 — RAG, phase 1 : indexation (hors ligne)** : documents → découpage en chunks → encodeur de phrases → index vectoriel.
- **Slide 4 — RAG, phase 2 : interrogation (en ligne)** : question → **même encodeur** → vecteur de requête → recherche top-k dans l'index → prompt (question + passages) → LLM → réponse **avec sources**.
- **Slide 5 — qui traite quoi** : chaque boîte renvoie au cours 6, 7, 8 ou 9.
- **Formules** : aucune (pas de `rappel@k` ici — reporté au cours 7).
- **Transition** : synthèse et vérification.
- **Acquis** : nommer les limites, expliquer pourquoi la même phrase change de vecteur selon le contexte, décrire les **deux phases** du RAG et la différence entre retrieval et génération.

### S8 — Synthèse et vérification (8 min, 3 slides)

- **Objectif** : consolider, vérifier, annoncer le TP.
- **Contenu** :
  - carte mentale (texte → tokens → représentation → similarité → sens → contexte) ;
  - **exercice de jugement** (et non récitation) : « Pour chacune de ces trois situations — rechercher `voiture` dans un catalogue qui dit `automobile`, retrouver un document qui parle de `avocat` au sens de fruit, répondre à une question dont les mots sont tous inconnus du corpus — dites quelle représentation vous choisissez et quelle limite vous acceptez. » ;
  - annonce du TP en 3 blocs.
- **Acquis** : l'étudiant sait choisir une représentation et en énoncer le prix.

### Récapitulatif du minutage

| Séquence | Durée | Slides |
|---|---|---|
| S0 Ouverture | 3 min | 3 |
| S1 Difficulté du langage | 7 min | 4 |
| S2 Texte → tokens | 19 min | 8 |
| S3 Distance d'édition | 15 min | 8 |
| S4 BoW + cosinus | 24 min | 12 |
| S5 TF-IDF | 15 min | 7 |
| S6 Word2Vec | 22 min | 9 |
| S7 Limites + RAG | 11 min | 5 |
| S8 Synthèse | 8 min | 3 |
| **Contenu** | **124 min** | **59** |
| Interactions, démos, transitions, imprévus | 26 min | — |
| **Total** | **150 min = 2 h 30** | **58** |

58 slides pour 122 minutes de contenu = 2 min 06 s par slide en moyenne, **hors** les 28 minutes d'interaction. C'est cohérent avec le cours 4 (45 pages pour un contenu homogène).

---

## 5. TP — 1 heure

**Format** : notebook Jupyter exécutable, environnement **préinstallé et testé hors ligne**, ressources embarquées dans `tp/data/`, 3 blocs notés + 1 exercice optionnel.

### Environnement

- `requirements.txt` avec versions figées, installé **avant** la séance (pas de `pip install` pendant le TP).
- Ressources locales : `corpus_fr.txt` (30 textes courts), `stopwords_fr.txt`, `embeddings_fr_mini.vec` (5 000 mots × 100 dimensions, pré-calculé une fois pour toutes et commité — aucun téléchargement, aucun entraînement bruyant).
- `nltk` et `spacy` **ne sont pas requis** : tout le prétraitement se fait en `re` + `unicodedata`, conformément à S2.

### Déroulé

| Bloc | Durée | Contenu | Acquis visé |
|---|---|---|---|
| **1 — Prétraitement** | 15 min | `normalize()` et `tokenize()` fournies **à trous** (2 lignes à écrire chacune) ; chargement des stop words depuis `data/` ; mesure du vocabulaire avant/après ; 4 questions d'interprétation (dont une sur la liste de stop words accentuée, laissée telle quelle à dessein) | Relier chaque décision de S2 à son effet mesuré |
| **2 — BoW, TF-IDF, cosinus** | 20 min | `CountVectorizer` puis `TfidfVectorizer` ; classement d'une requête ; requête volontairement OOV → vecteur nul ; comparaison des deux classements | Comprendre `fit`/`transform` et le vecteur nul |
| **3 — Embeddings pré-calculés** | 12 min | `KeyedVectors.load_word2vec_format` sur `embeddings_fr_mini.vec` ; plus proches voisins de 3 mots ; une analogie ; un échec (polysémie `avocat`) ; comparaison avec le classement TF-IDF du bloc 2 | Voir la différence lexical/dense **sur des données réelles** |
| **Marge** | 13 min | Lecture des consignes, erreurs d'exécution, sauvegarde, questions | — |
| **Optionnel (hors séance)** | — | Implémenter la matrice de Levenshtein complète ; comparer à `difflib.SequenceMatcher` **en expliquant que ce n'est pas Levenshtein** (algorithme de Ratcliff/Obershelp) | Approfondissement pour les plus rapides |

### Livrables du TP (phase 5)

`tp/tp5_enonce.md`, `tp/tp5_etudiant.ipynb`, `tp/tp5_corrige.ipynb`, `tp/data/{corpus_fr.txt, stopwords_fr.txt, embeddings_fr_mini.vec}`, `tp/requirements.txt`, `tp/README.md` (installation, versions, résultats attendus).

### Contraintes de production

- Le notebook sera **exécuté intégralement** (kernel neuf) avant livraison ; les sorties affichées seront celles de cette exécution.
- Les résultats du bloc 2 sont **déjà connus et vérifiés** (voir S4/S5) : le corrigé indiquera les valeurs attendues.
- Le fichier `embeddings_fr_mini.vec` sera produit lors de la phase 5 à partir d'un corpus français public, tronqué à 5 000 mots les plus fréquents ; il doit rester sous 5 Mo.

---

## 6. Progression proposée pour les cours 6 à 9

| Cours | Titre | Contenu | Lien avec le cours 5 |
|---|---|---|---|
| **6** | Embeddings modernes et Transformers | Attention (Q/K/V), BERT vs GPT, `sentence-transformers`, pooling, similarité entre phrases, POS et NER | Reprend S6 (projection) et S7 (polysémie) ; traite ce qui a été reporté |
| **7** | Recherche sémantique et bases vectorielles | Chunking, jugement de pertinence, `rappel@k`, MRR, HNSW, FAISS, pgvector, hybride BM25 + dense | Réutilise TF-IDF (S5) comme baseline et le cosinus (S4) comme mesure |
| **8** | RAG avec LangChain | Loaders, splitters, vectorstore, retriever, prompt, LCEL, chaîne complète question → réponse citée | Les deux phases de S7 deviennent le plan du cours |
| **9** | Évaluer et industrialiser un RAG | Jeu d'évaluation, fidélité, pertinence, coûts, latence, garde-fous, observabilité | Les limites de S3–S7 deviennent les critères d'évaluation |

Chaque brique du RAG aura été construite à la main avant d'être appelée via une bibliothèque : c'est la condition pour ne pas faire un « RAG de façade ».

---

## 7. Arbitrages sur la revue Codex

Revue complète : `Cours_5/notes/revue-codex-v1.md` (Codex `gpt-5.6-sol`, `reasoning_effort=xhigh`). Verdict v1 : **À RESTRUCTURER** sur 4 séquences (S2, S3, S6, S7), **À CORRIGER** sur 4 autres (S0, S4, S5, S8), **VALIDÉ** sur S1.

| Remarque Codex | Décision | Traitement en v2 |
|---|---|---|
| 73 slides irréalistes, 145 min sans marge | **Acceptée** | 54 slides, 120 min + 30 min d'interaction explicites |
| S2 cumule plus de 12 notions | **Acceptée** | 7 slides, POS réduit à 3 lignes, Unicode réduit à une démo |
| Construction complète de la matrice de Levenshtein en 4 slides | **Acceptée** | 1 slide « matrice remplie » ; construction en annexe + TP optionnel |
| Mélange des conventions TF-IDF | **Acceptée** | Convention sklearn unique, tous les exemples recalculés |
| « TF-IDF change le classement » sur `le chat` | **Acceptée** | Remplacé par `félin salon`, inversion réellement vérifiée |
| « D3 devrait être premier sur le sens » | **Acceptée** | Supprimé ; remplacé par la démonstration du vecteur nul (OOV) |
| Formule softmax sans prérequis | **Acceptée** | Formule d'agrégation seule ; softmax renvoyé au cours 6 |
| `|V| × d` sous-estime le coût | **Acceptée** | `2 × 10⁶` poids (entrée + sortie) |
| Exemple de polysémie `banque` invalide en français | **Acceptée** | `avocat`, `glace`, `vol` |
| Pipeline RAG à 6 boîtes incomplet | **Acceptée** | 2 phases, 10 éléments, encodage de la requête et génération inclus |
| TP infaisable, dépendances non garanties, Word2Vec non interprétable sur 2 000 mots | **Acceptée** | 3 blocs, environnement préinstallé, embeddings pré-calculés |
| Accroche « 0 mot commun » | **Acceptée** | Reformulée : 2 mots outils, 0 mot porteur de sens |
| `[A-Za-zÀ-ÿ]+` incorrect | **Acceptée** | Remplacé par `\w+`, avec démonstration de ses limites |
| S1 : quatre sources vs liste de cinq | **Acceptée** | Liste close de 4, niveaux d'analyse séparés |
| Paire `(dort, canapé)` hors fenêtre 2 | **Refusée** | Indices 2 et 4 → écart de 2, donc **dans** la fenêtre. L'exemple est conservé, mais réécrit avec les indices visibles sur la slide |
| `SequenceMatcher` ≠ Levenshtein | **Acceptée** | Mention explicite (Ratcliff/Obershelp) dans l'exercice optionnel |
| « Tous les cursus sérieux » | **Acceptée** | Reformulé en « convergence partielle » avec les divergences nommées |
| `rappel@k` avant jugement de pertinence | **Acceptée** | Retiré de ce cours, reporté au cours 7 |
| S8 trop court pour 5 questions | **Acceptée** | 8 min, 3 slides, une seule question de jugement à 3 cas |

---

## 8. Décisions validées le 2026-11-02

| Question | Décision |
|---|---|
| Volume | **54 slides** (dont 30 min d'interaction) — **58 à la livraison** : voir le budget révisé du §4 |
| POS tagging | **3 lignes** dans le slide pipeline |
| Levenshtein | **Construction pas à pas dans le tronc** (+4 min sur S3, compensés sur S1, S4, S5 et S6) |
| Embeddings du TP | **Fichier pré-calculé commité** (~5 Mo, 5 000 mots × 100 dimensions) |
| Corpus d'exemple | 4 phrases jouets (chat / chien / félin / salon) — **à reconfirmer** si un corpus métier est préféré |

---

## 9. Transparence sur l'état d'avancement

| Élément | État |
|---|---|
| Audit des cours 1–4 | ✅ réalisé sur les fichiers du dépôt |
| Analyse des 2 supports fournis (`06-DL_05-Natural-Language-Processing.pdf`, `06-DL_05-Transformers.pdf`) | ✅ textes extraits et lus |
| Ressource CentraleSupélec CM1 (80 pages) | ✅ téléchargée et analysée |
| Recherche de progressions (Jurafsky, CMU, CS224N, Hugging Face) | ✅ pages sources consultées |
| Capacités MARP | ✅ testées réellement (`marp-cli v4.5.1`, PDF + HTML de test) |
| Chiffres des exemples (Levenshtein, cosinus, IDF, inversion de classement) | ✅ calculés et vérifiés par script (scikit-learn) |
| Revue critique Codex | ✅ effectuée — verdict v1 : À RESTRUCTURER — 19 remarques traitées (18 acceptées, 1 refusée avec justification) |
| Plan révisé (v2.1) | ✅ validé le 2026-11-02 |
| Validation humaine | ⏳ en attente |
| Slides S0–S8 (58 slides) | ✅ produits ; **PDF à recompiler** après l'ajout de la slide d'objectifs, et contrôle visuel à refaire sur les deux slides nouvelles |
| Revue Codex blocs 1 à 4 | ✅ 3 revues, 43 corrections appliquées |
| Revue blocs 5 à 8 | ⚠️ Codex indisponible (quota) — revue par sous-agent indépendant + script de vérification numérique |
| TP (énoncé, notebook, corrigé, données) | ✅ corrigé exécuté intégralement, sorties réelles |
| Rapport de validation | ✅ `Cours_5/notes/rapport-validation.md` |
