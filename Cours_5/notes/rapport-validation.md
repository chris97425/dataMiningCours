# Rapport de validation — Cours 5

**Projet** : `dataMiningCours/Cours_5` · **Date** : 2026-11-02 · **Auteur** : Christopher de Boisvilliers
**Périmètre** : plan pédagogique, 60 slides MARP, TP d'une heure. **Partie RAG retirée** le 2026-11-02 à la demande de l'auteur.

---

## 1. Chaîne de validation réellement suivie

| Étape | Outil | Verdict | Traitement |
|---|---|---|---|
| Plan v1 (18 objectifs) | Codex `gpt-5.6-sol`, `reasoning_effort=xhigh` | **À RESTRUCTURER** (4 séquences) | 19 remarques : 18 acceptées, 1 refusée avec preuve |
| Plan v2 → décisions utilisateur | — | Validé le 2026-11-02 | 54 slides, Levenshtein dans le tronc, embeddings pré-calculés |
| Bloc 1 (S0–S1, 6 slides) | Codex | **À CORRIGER** | 5 corrections appliquées (comptage 13/10, surlignage, schéma RAG, etc.) |
| Blocs 2–3 (S2–S3, 15 slides) | Codex | **À CORRIGER** | 27 corrections appliquées (matrices, récurrence, stop words, stemming, POS, regex, limites) |
| Bloc 4 (S4, 10 slides) | Codex | **À CORRIGER** | 11 corrections (normes L2, calcul de 0,671, bigrammes, vecteur nul, fréquence documentaire) |
| Blocs 5–8 (S5–S8, 23 slides) | Codex **indisponible** (quota atteint à 12:35, réinitialisation 17:04) → revue indépendante par sous-agent + script de vérification `notes/verif_slides32_54.py` | **À CORRIGER** sur S5, S6, S7 — S8 validé. 100 % des valeurs numériques reproduites ; 6 erreurs de fond relevées, toutes corrigées | Corrections appliquées : voir §2 bis |

**Transparence** : les blocs 5 à 8 n'ont **pas** été relus par Codex. Ils ont été vérifiés par (a) un sous-agent indépendant qui a recalculé toutes les valeurs avec scikit-learn, (b) une relecture ciblée des formules et du schéma RAG. C'est une revue plus faible que les précédentes et cela doit être dit.

---

## 2. Corrections notables (les plus lourdes)

| # | Problème détecté | Correction |
|---|---|---|
| 1 | « 10 mots » pour deux phrases qui en comptent 13 occurrences / 10 formes | Comptage exact affiché, distinction occurrence / forme introduite |
| 2 | Schéma de la chaîne terminé par « Sens / contexte », comme si le cosinus produisait le sens | Chaîne réduite à 4 briques ; le contexte renvoyé explicitement à la séance 6 |
| 3 | Matrice de Levenshtein décalée d'une colonne (en-tête `ε` manquant) | En-tête reconstruit, alignement vérifié visuellement |
| 4 | Candidats haut/gauche inversés sur la slide de remplissage | Case (a, a) recalculée : haut 1+1=2, gauche 2+1=3, diagonale 0+0=0 |
| 5 | « Levenshtein ignore l'ordre » | Faux : la distance est au contraire très sensible à l'ordre ; formulation corrigée |
| 6 | TF-IDF : deux conventions mélangées (tf relatif vs tf brut sklearn) | Convention sklearn unique : tf brut, idf lissé, normalisation L2 ; tous les exemples recalculés |
| 7 | « `le` pèse six fois plus que `félin` dans le cosinus » | Confusion fréquence / contribution ; réécrit autour de la **fréquence documentaire** (3/4 vs 1/4) |
| 8 | Cosinus d'un vecteur nul présenté comme « 0 par définition » | Indéfini (0/0) ; scikit-learn renvoie 0 **par convention** |
| 9 | « `voiture` et `automobile` : aucune lettre en commun » | Faux ; remplacé par « distance 8 sur 10 » |
| 10 | Formule softmax de Word2Vec sans prérequis (aucune couche neuronale au cours 4) | Formule d'agrégation seule ; softmax renvoyé au cours 6 |
| 11 | Coût Word2Vec sous-estimé (`|V|×d` seulement) | Deux matrices : ≈ 2×10⁶ poids pour 10k×100 ; 60 M pour 100k×300 |
| 12 | Exemple de polysémie `banque` (transposition de l'anglais *bank*) | Remplacé par `avocat` (fruit / métier), vérifié dans les vecteurs du TP |
| 13 | Pipeline RAG « 6 boîtes » incomplet (requête non encodée, pas de génération) | Deux phases, 10 éléments, encodage de la requête et réponse sourcée inclus |
| 14 | TP irréaliste (6 exercices, 60 min pile, Word2Vec non interprétable sur 2 000 mots) | 3 blocs (15 + 20 + 12 min) + 13 min de marge, embeddings pré-calculés |
| 15 | `SequenceMatcher` présenté comme Levenshtein | Mention explicite : Ratcliff/Obershelp, algorithme différent |

---

## 2 bis. Corrections issues de la revue indépendante (blocs 5–8)

> Les numéros de slide de ce tableau sont ceux de la version à **55 pages**. Trois slides ont été insérées depuis (p. 3 « Objectifs de la séance », « Le sac, mécaniquement » et « Remplir les cases : présence ou comptage ? ») : les pages ≥ 27 ont glissé de +3.

| # | Problème | Correction |
|---|---|---|
| 1 | Slide 47 : « mots inconnus → vecteur nul » confondait mot hors vocabulaire (qui n'a **aucun** vecteur) et expression multi-mots (sens non compositionnel) | Tableau scindé en 5 lignes ; « Word2Vec a réglé » → « **atténue** » |
| 2 | Slide 43 : « 60 M de paramètres, c'est pour cela que l'échantillonnage… » — causalité fausse | Le coût réduit par le negative sampling est le **calcul des |V| scores**, pas le nombre de paramètres |
| 3 | Slide 42 : `|C| = 2k` faux près des bornes (contredit la slide 40) | `|C| ≤ 2k` ; matrice d'entrée vs matrice de sortie explicitée |
| 4 | Slide 33 : « facteur global » faux — le facteur est **par document**, et les cosinus sont **identiques** après L2 | Reformulé |
| 5 | Slide 34 : « deux fois moins » alors que 1,916 / 1,223 = **1,57** | Corrigé |
| 6 | Slide 37 : « aucune stabilité » trop absolu | « très instable (forte variance) » |
| 7 | Slide 40 : paires orientées façon Skip-gram avant que CBOW ne soit introduit | Associations mot ↔ contexte, sans direction |
| 8 | Aucune référence bibliographique | Salton & Buckley (1988), Mikolov et al. (2013), Lewis et al. (2020) ajoutées en pied de section |
| 9 | Slide 43 : dimension 100–300 non justifiée | Ajouté : compromis capacité / coût |

---

## 3. Vérifications numériques exécutées

Script : `Cours_5/notes/verif_slides32_54.py` (scikit-learn 1.6.1).

| Grandeur | Valeur annoncée | Vérifiée |
|---|---|---|
| `idf(le)` / `idf(salon)` | 1,223 | ✅ |
| `idf(dort)` | 1,511 | ✅ |
| `idf(chat)` / `idf(félin)` | 1,916 | ✅ |
| cosinus TF-IDF « le chat » | 0,641 / 0,288 / 0 / 0,214 | ✅ |
| « félin salon » comptages | D4 = 0,365 en tête | ✅ |
| « félin salon » TF-IDF | D3 = 0,291 en tête, D4 = 0,214 | ✅ |
| matrice de comptage | 26 cellules non nulles / 72 | ✅ |
| Levenshtein `chat`→`chats` | 1 | ✅ |
| `chien`/`chats`, `voiture`/`automobile` | 3 et 8 | ✅ |
| taille du TP | 30 textes, 282 mots, 5000 vecteurs × 100 d | ✅ (4,2 Mo) |

Le corrigé du TP a été **exécuté intégralement** (11 cellules, sorties réelles injectées). Sorties clés :

- BoW « le chat » : 0,535 / 0,316 / 0,289
- TF-IDF : 0,471 / 0,300 / 0,234 → **le classement change** (le document « chien » passe devant un document « chat »), ce qui illustre réellement l'effet de la pondération
- Requête « gâteau au chocolat » : 0 mot reconnu, norme 0,0, scores nuls
- Embeddings : `chat` → félin 0,72 · chien 0,62 ; `avocat` → légiste 0,77, avocate 0,70 (un seul sens : la limite est démontrable en séance)

---

## 4. Contrôle du rendu

- Export PDF : 60 pages, format 4:3 (720 × 540 pt), `marp-cli 4.5.1`, thème `neobeam` — compilé et vérifié après chaque ajout de slide.
- **Piège technique documenté** : Marp CLI exige `--html` **et** `--allow-local-files` ; sans `--html`, tous les `<div>` sont aplatis (premier rendu cassé, corrigé).
- Planche de contrôle (`notes/planche-59-slides.png`) inspectée sur la version à 59 slides : aucun débordement, aucun texte tronqué. Les slides ajoutées (objectifs, sac mécanique, présence/comptage, POS, rareté IDF) ont été contrôlées une par une.
- Cinq SVG locaux utilisés (`niveaux-analyse`, `pipeline-cours5`, `bow-mecanique`, `cosinus`, `word2vec-plan`). Les deux SVG d'analogie devenus inutiles (`analogie-espace-embeddings`, `analogie-parallelogramme`) ont été supprimés — récupérables dans l'historique Git. Deux images bitmap : `bow-sac.jpg` (Wikimedia Commons, domaine public, crédit affiché sur la slide) et `analogie-embedding-space.png` (figure externe créditée « @akshay_pachaar » — **licence à préciser** avant toute diffusion hors cours).

---

## 5. Limites assumées

1. **Blocs 5 à 8 non relus par Codex** (quota) : revue indépendante par sous-agent, plus faible qu'une revue Codex complète.
2. **Pas de test en amphithéâtre** : les 122 minutes de contenu sont une estimation construite, pas une mesure.
3. **Corpus du TP volontairement minuscule** (282 mots) : les scores illustrent des mécanismes, pas des performances ; l'IDF sur 30 documents n'a aucune stabilité.
4. **Embeddings du TP** : `fr_core_news_md` tronqué à 100 dimensions et 5 000 mots — qualité suffisante pour les exercices, insuffisante pour des conclusions scientifiques.
5. **Illustrations** : les schémas sont des SVG maison, mais **deux images ne le sont pas** — `bow-sac.jpg` (Wikimedia Commons, domaine public) et `analogie-embedding-space.png` (figure externe, crédit d'auteur sans licence explicite). Aucune animation.

---

## 6. État des livrables

| Livrable | Fichier | État |
|---|---|---|
| Plan pédagogique | `Cours_5/PLAN_PEDAGOGIQUE.md` | ✅ v2.2, alignée sur le cours réellement produit |
| Cours 5 (60 slides) | `Cours_5/presentation.md` | ✅ |
| Export PDF | `Cours_5/presentation.pdf` | ✅ 60 pages |
| Thème | `Cours_5/themes/neobeam.css` | ✅ identique au cours 4 |
| Illustrations | `Cours_5/images/` | ✅ 5 SVG + 2 bitmaps |
| Énoncé TP | `tp/tp5_enonce.md` | ✅ |
| Notebook étudiant | `tp/tp5_etudiant.ipynb` | ✅ |
| Corrigé exécuté | `tp/tp5_corrige.ipynb` | ✅ 11 cellules exécutées + 1 note enseignant ; le code de calcul n'a pas été modifié, les sorties restent valides |
| Données | `tp/data/` | ✅ corpus, stop words, embeddings (4,2 Mo) |
| Installation | `tp/README.md`, `tp/requirements.txt` | ✅ |
| Progression séances 6–9 | `PLAN_PEDAGOGIQUE.md` §6 | ✅ |
| Rapport de validation | ce fichier | ✅ |

---

## 7. Contrôle de cohérence du 2026-11-02 (passe finale)

**Méthode** : relecture intégrale de `presentation.md`, du plan, du TP et des notes ; **toutes les valeurs numériques ont été recalculées indépendamment** (script Python, `scikit-learn 1.6.1` / `numpy 2.0.2`, et relecture directe des 5 000 vecteurs du TP sans `gensim`).

**Revérifié et confirmé — aucune correction nécessaire** :

- corpus d'exemple : 18 termes ; matrice 26 cases non nulles sur 72 (36 %) ; `le` = 6 occurrences dans 3 documents sur 4, `salon` 4 dans 3 sur 4, `félin` 1 dans 1 sur 4 ;
- cosinus BoW « le chat » 0,671 / 0,447 / 0 / 0,365 et TF-IDF 0,641 / 0,288 / 0 / 0,214 ; « animal de compagnie » = 0 partout ;
- IDF 1,223 / 1,511 / 1,916 ; « félin salon » 0,224 / 0,224 / 0,236 / 0,365 → TF-IDF 0,144 / 0,144 / 0,291 / 0,214 ;
- Levenshtein 1 / 1 / 3 / 2 / 8 et similarités normalisées 0,80 / 0,86 / 0,40 / 0,80 / 0,20 ;
- matrice `chat → chats` : case (a,a) = 0 (haut 1+1, gauche 1+1, diagonale 0+0), dernière case = 1, chemin optimal correct ;
- Word2Vec : 2 × 10⁶ et 60 × 10⁶ paramètres ; fenêtre de `dort` = {le, chat, sur, canapé} (écarts 2, 1, 1, 2) ;
- TP : sorties des blocs 1 et 2 **reproduites à l'identique** (0,535 / 0,316 / 0,289 ; 0,471 / 0,300 / 0,234 ; norme 0,0) ; `cos(reine − roi, femme − homme)` = **0,3726** ; voisins de `chat` : félin 0,717 · chien 0,618 · chats 0,615.

**Corrections appliquées aux slides** :

| # | Défaut relevé | Correction |
|---|---|---|
| 1 | Le bandeau de la section 3 (« Mesurer la ressemblance ») ne reprenait pas l'intitulé annoncé dans le plan de la séance | Bandeau → « Distance d'édition » ; item 6 du plan → « Des mots aux vecteurs (Word2Vec) » ; bandeau 7 → « Limites et préparation au RAG » |
| 2 | Renvois internes `S3` … `S7`, sigle jamais défini (et confondable avec « séance 6 ») | Écrits en clair : « section 3 » … « section 7 » |
| 3 | Aucune slide d'objectifs, alors que le cours 4 en a une | Slide « Objectifs de la séance » (5 objectifs en verbes d'action, rattachés à leur section, + prérequis) |
| 4 | « la slide précédente » renvoyait à une slide sans aucun chiffre | « la slide « Ce que ça donne » » |
| 5 | « Ces 0,37 ne sont pas une similarité » (accord) | « Ce 0,37 n'est pas une similarité » |
| 6 | Deux puces redondantes sur les stop words, avec une causalité fausse | Réécrites : gain de dimensions / gain de bruit |
| 7 | « dimension : 100 à 300 — … au-delà les gains… » (ponctuation) | Point-virgule + virgule |
| 8 | « les 13 minutes restantes sont la lecture des consignes » | « sont consacrées à la lecture des consignes, aux erreurs… » |
| 9 | En-tête de colonne « Comptages » pour des cosinus (slide TF-IDF) | « Cosinus (comptages) » / « Cosinus (TF-IDF) », comme la slide suivante |
| 10 | « il ne sépare au mieux que D3 des trois autres » (ambigu) | « il ne peut, au mieux, que distinguer D3 des trois autres » |
| 11 | Bigramme `mord homme` incompatible avec la découpe en tokens retenue | `mord l'homme` |
| 12 | « Stemming (radical) » contredisait la glose « un stem n'est pas un radical » | « Stemming (stem produit) » |
| 13 | « Plus lent » pour la lemmatisation (accord) | « Plus lente » |
| 14 | « token = un mot » (slide 3) contredisait « ici token ne veut plus dire mot » (fin de S2) | « c'est le même terme, mais pas la même unité » + « avec les sous-mots, « token » ne veut plus dire « mot » » |
| 15 | Le `+1` de l'IDF justifié par une division par zéro impossible (`df ≥ 1`) | « les +1 lissent le rapport : l'IDF ne peut jamais être nul ni négatif » |
| 16 | `w_t` employé dans la formule CBOW sans définition, et `contexte \ {w_t}` vide par construction | `C = contexte(w_t), w_t ∉ C` + glose « w_t = le mot central, la cible » |
| 17 | « il n'y a pas de couche « cachée » séparée » (contredit la couche *h*) | « la couche intermédiaire n'est que la moyenne de ces lignes » |
| 18 | Voisins de `chat` cités (`matou`) absents du vocabulaire du TP — l'étudiant ne pouvait pas vérifier | Valeurs du TP ajoutées sous la phrase : `félin` 0,72 · `chien` 0,62 · `chats` 0,62 |
| 19 | « un chunk » employé avant sa glose | « un chunk (un passage de document) » |
| 20 | « l'ordre et le contexte disparaissent » (le pooling ne retire pas de contexte à des vecteurs statiques) | « l'ordre et les relations entre mots » |
| 21 | Entrée « 5 · NLP : du texte au sens » ≠ titre du cours | « 5 · NLP : du texte aux vecteurs » |

**Corrections appliquées aux documents annexes** :

- **Plan** : 54/55/56/57 slides → **58** ; budget 122 min de contenu + 28 min d'interaction ; valeur `félin` 0,378 → **0,333** ; « 2 questions » → 4 ; accroche des deux phrases rattachée à S1 ; note sur les écarts de front-matter (2026, `html: true`, `title`).
- **TP** : « La requête contient quatre mots » → la requête en compte **six** tokens ; l'énoncé annonçait `animal de compagnie` alors que le notebook utilise `gâteau au chocolat` ; **question 4** ajoutée sur la liste de stop words accentuée (défaut volontaire, documenté dans le README et dans une note enseignant du corrigé) ; prérequis et installation ajoutés à l'énoncé ; `requirements.txt` réellement figé ; « section S2 » → « section 2 » ; `docs = tokenize_corpus = …` nettoyé.
- **Ce rapport** : « quatre SVG » annoncés avec quatre noms, mais six existent ; « aucune image externe » contredit `bow-sac.jpg` et `analogie-embedding-space.png`.

**Points laissés à l'arbitrage de l'auteur** :

1. `analogie-embedding-space.png` : crédit d'auteur affiché sur la slide, mais **licence non explicite** — à préciser avant toute diffusion publique du support.
2. Espaces insécables avant `:` `?` `!` `;` : absents du fichier (~140 occurrences) et absents des cours 1 à 4 — correction globale à décider.
3. Gloses de `rappel@k`, HNSW et « fidélité » sur la slide « Qui traite quoi ».
4. Recompilation du PDF et contrôle visuel des trois slides ajoutées.
