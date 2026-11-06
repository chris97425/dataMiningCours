# Cours 5 — Du texte aux vecteurs

**Data Mining · Christopher de Boisvilliers · Esiroi 2026**

Ce dossier est la **version compétences** du cours 5. Le contenu technique est celui du cours existant (`Cours_5/`), vérifié numériquement en novembre 2026. Ce qui change ici, c'est la charpente : ce que vous saurez **faire**, comment vous le saurez, et quand vous le réviserez.

---

## Ce que vous saurez faire

Six capacités. Ce ne sont pas des objectifs en « comprendre » : chacune se voit dans un travail rendu.

| # | Capacité | En une phrase | Section |
|---|---|---|---|
| **C1** | Prétraiter en justifiant | Produire des tokens d'un texte français brut en nommant ce que chaque décision fait perdre | S2 |
| **C2** | Mesurer une similarité de surface | Remplir une matrice de Levenshtein à la main et dire pourquoi elle ignore le sens | S3 |
| **C3** | Vectoriser et classer | Construire une matrice documents × termes, calculer les cosinus, expliquer un score nul | S4 |
| **C4** | Pondérer et anticiper | Calculer un IDF sklearn et **prédire** si TF-IDF change un classement | S5 |
| **C5** | Expliquer Word2Vec en bornant sa portée | Énoncer l'hypothèse distributionnelle, distinguer CBOW/Skip-gram, nommer quatre limites | S6 |
| **C6** | Choisir une représentation | Devant trois situations, choisir, justifier, et nommer la limite acceptée | S7–S8 |

**C6 est la capacité terminale.** C1 à C5 sont des moyens. Si vous ne devez retenir qu'une chose de ce cours : savoir choisir, et savoir dire ce que vous perdez en choisissant.

Détail complet, avec situations et standards : `CAPABILITIES.md`.

---

## Prérequis, et comment les vérifier vous-même

Ce cours suppose les cours 1 à 4. Cinq vérifications, 5 minutes, réponses en `answers/tickets-et-cfu.md` § Diagnostic.

| # | Question | Où c'était |
|---|---|---|
| 1 | Produit scalaire de `[1,2,3]` et `[1,1,1]` ? Norme de `[1,2,3]` ? | Cours 2 |
| 2 | La sigmoïde pour un score de 0, c'est combien ? | Cours 4 |
| 3 | 40 vrais positifs, 10 faux négatifs, 5 faux positifs : rappel ? | Cours 4 |
| 4 | `fit` puis `predict` : quelle différence ? | Cours 2 |
| 5 | Pourquoi standardiser une colonne avant un modèle linéaire ? | Cours 2 |

**Si vous ratez l'item 1**, reprenez le produit scalaire avant la séance : le cosinus de S4 en dépend entièrement. Les quatre autres peuvent se rattraper en cours de route.

**Ce qui n'est *pas* requis** : aucune connaissance en linguistique, aucune notion de réseau de neurones, pas de softmax, pas de couche cachée. Le cours 4 s'arrête à la régression logistique et ce cours est construit pour partir de là.

---

## Carte des modules

```
S0 Ouverture ─────────────────────────── contrat + diagnostic
   │
S1 Pourquoi le texte pose problème ──── 4 sources, 4 niveaux     [prérequis C6]
   │
S2 Du texte aux tokens ──────────────── C1  prétraiter
   │
S3 Distance d'édition ───────────────── C2  comparer des chaînes
   │
S4 Sac de mots et cosinus ───────────── C3  vectoriser et classer
   │
S5 TF-IDF ───────────────────────────── C4  pondérer et anticiper
   │
S6 Des mots aux vecteurs ────────────── C5  Word2Vec
   │
S7 Limites et RAG ───────────────────── C5 → C6
   │
S8 Synthèse et transfert ────────────── C6  choisir          ← la cible
```

Chaque section se termine par un **ticket de sortie** de 90 secondes, qui mêle la section courante et une section antérieure. Ce n'est pas un contrôle : c'est le mécanisme d'apprentissage le plus efficace connu, et il ne fonctionne que si vous écrivez avant de vérifier.

---

## Comment suivre ce cours

Quatre règles. Elles ne sont pas des conseils de méthode : ce sont les conditions sans lesquelles la séance ne produit rien de durable.

**1. Tentez avant de lire l'explication.**
Chaque section commence par une prédiction ou une tentative. Elle est souvent fausse — c'est prévu. Une tentative ratée suivie de la correction produit plus de rétention qu'une explication claire lue sans effort. **Ne sautez pas ces slides parce qu'elles vous ralentissent.**

**2. Écrivez, ou dites à voix haute.**
Décider « je le sais » ne compte pas. Le rappel doit être produit : sur papier, ou dit à votre voisin. C'est l'acte de production qui consolide, pas la sensation de reconnaissance.

**3. Donnez votre confiance avant de vérifier.**
« Sûr / probable / au hasard. » Cette étiquette vaut plus que la réponse : une erreur dont vous étiez sûr révèle une conception fausse, qu'il faut aller déloger. Une erreur dont vous doutiez est juste un trou de mémoire. Les deux ne se réparent pas de la même façon.

**4. Suivez `review-schedule.md`.**
J+1, J+7, J+21 — trois créneaux, 15 à 18 minutes chacun. Chacun est une **récupération**, jamais une relecture. Si vous ne faites qu'une chose après ce cours, faites le J+1 : c'est le créneau où la courbe de l'oubli est la plus raide.

---

## Ce que contient ce dossier

| Fichier | À quoi il sert |
|---|---|
| `00-syllabus.md` | Ce document — capacités, prérequis, carte, méthode |
| `CAPABILITIES.md` | Les six capacités en détail : quoi, dans quelle situation, à quel standard, comment on le voit |
| `PLAN_PEDAGOGIQUE_v3.md` | La conception : résultats visés, preuves, progression, analyse de charge, estompage, minutage, alignement |
| `presentation.md` | Les 79 slides MARP (tentative → principe → exemple → estompage → ticket) |
| `presentation.pdf` | Le même, exporté pour projection |
| `TICKETS_ET_CFU.md` | **Document du professeur** : les items, et pour chaque réponse d'étudiant ce qu'elle révèle et quel est le prochain geste |
| `answers/` | Les réponses. À n'ouvrir qu'après avoir écrit la sienne |
| `GRILLE_TP.md` | La grille du TP : quatre critères, quatre niveaux, version professeur et version étudiant |
| `review-schedule.md` | Le calendrier de révision espacée, J+1 à J+21, et son prolongement sur les séances 6 à 9 |
| `tp/` | Le TP inchangé : énoncé, notebook étudiant, corrigé, données |
| `images/`, `themes/` | Ressources du thème `neobeam` (4:3) |

---

## Durée et format

| | |
|---|---|
| Cours | 2 h 30 — 135 min de contenu, dont les tentatives, 15 min de transitions |
| TP | 1 h — 3 blocs (15 / 20 / 12 min) + 13 min de marge |
| Format | MARP, thème `neobeam`, 4:3, MathJax, export PDF |
| Slides | 79 |

**Le temps des tentatives n'est pas du temps perdu.** Il est compté dans les 135 minutes de contenu, parce qu'une tentative de 60 secondes produit plus d'apprentissage qu'une slide de plus.
