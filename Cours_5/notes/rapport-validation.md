# Rapport de validation — Cours 5

**Projet** : `dataMiningCours/Cours_5` · **Date** : 2026-11-02 · **Auteur** : Christopher de Boisvilliers
**Périmètre** : plan pédagogique, 54 slides MARP, TP d'une heure.

---

## 1. Chaîne de validation réellement suivie

| Étape | Outil | Verdict | Traitement |
|---|---|---|---|
| Plan v1 (18 objectifs) | Codex `gpt-5.6-sol`, `reasoning_effort=xhigh` | **À RESTRUCTURER** (4 séquences) | 19 remarques : 18 acceptées, 1 refusée avec preuve |
| Plan v2 → décisions utilisateur | — | Validé le 2026-11-02 | 54 slides, Levenshtein dans le tronc, embeddings pré-calculés |
| Bloc 1 (S0–S1, 6 slides) | Codex | **À CORRIGER** | 5 corrections appliquées (comptage 13/10, surlignage, schéma RAG, etc.) |
| Blocs 2–3 (S2–S3, 15 slides) | Codex | **À CORRIGER** | 27 corrections appliquées (matrices, récurrence, stop words, stemming, POS, regex, limites) |
| Bloc 4 (S4, 10 slides) | Codex | **À CORRIGER** | 11 corrections (normes L2, calcul de 0,671, bigrammes, vecteur nul, fréquence documentaire) |
| Blocs 5–8 (S5–S8, 23 slides) | Codex **indisponible** (quota atteint à 12:35, réinitialisation 17:04) → revue indépendante par sous-agent + script de vérification `notes/verif_slides32_54.py` | Valeurs numériques **reproduites à l'identique** | Vérification manuelle complémentaire des formules et du schéma RAG |

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

- Export PDF : 54 pages, format 4:3 (720 × 540 pt), `marp-cli 4.5.1`, thème `neobeam`.
- **Piège technique documenté** : Marp CLI exige `--html` **et** `--allow-local-files` ; sans `--html`, tous les `<div>` sont aplatis (premier rendu cassé, corrigé).
- Planche de contrôle des 54 slides inspectée : aucun débordement, aucun texte tronqué.
- Trois SVG produits pour le cours (`niveaux-analyse`, `pipeline-cours5`, `cosinus`, `word2vec-plan`), tous en local, aucun lien distant.

---

## 5. Limites assumées

1. **Blocs 5 à 8 non relus par Codex** (quota) : revue indépendante par sous-agent, plus faible qu'une revue Codex complète.
2. **Pas de test en amphithéâtre** : les 120 minutes de contenu sont une estimation construite, pas une mesure.
3. **Corpus du TP volontairement minuscule** (282 mots) : les scores illustrent des mécanismes, pas des performances ; l'IDF sur 30 documents n'a aucune stabilité.
4. **Embeddings du TP** : `fr_core_news_md` tronqué à 100 dimensions et 5 000 mots — qualité suffisante pour les exercices, insuffisante pour des conclusions scientifiques.
5. **Illustrations** : schémas SVG maison ; aucune image externe, donc aucune question de licence, mais pas de photographie ni d'animation.

---

## 6. État des livrables

| Livrable | Fichier | État |
|---|---|---|
| Plan pédagogique | `Cours_5/PLAN_PEDAGOGIQUE.md` | ✅ v2.1 validée |
| Cours 5 (54 slides) | `Cours_5/presentation.md` | ✅ |
| Export PDF | `Cours_5/presentation.pdf` | ✅ 54 pages |
| Thème | `Cours_5/themes/neobeam.css` | ✅ identique au cours 4 |
| Illustrations | `Cours_5/images/*.svg` | ✅ 4 SVG |
| Énoncé TP | `tp/tp5_enonce.md` | ✅ |
| Notebook étudiant | `tp/tp5_etudiant.ipynb` | ✅ |
| Corrigé exécuté | `tp/tp5_corrige.ipynb` | ✅ 11 cellules, sorties réelles |
| Données | `tp/data/` | ✅ corpus, stop words, embeddings (4,2 Mo) |
| Installation | `tp/README.md`, `tp/requirements.txt` | ✅ |
| Progression séances 6–9 | `PLAN_PEDAGOGIQUE.md` §6 | ✅ |
| Rapport de validation | ce fichier | ✅ |
