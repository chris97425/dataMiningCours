# Cours 5 — Capacités visées

**Version** : 1.0 · 2026-11-05
**Méthode** : `anything-to-course` (étape 1) — l'unité de conception n'est pas un sujet, c'est **une capacité nouvelle de l'apprenant**.
**Public** : licence / master appliqué, ayant suivi les cours 1 à 4. Aucune connaissance en linguistique supposée.
**Durée** : 2 h 30 de cours + 1 h de TP.

> **Règle directrice** : un contenu qui ne sert aucune capacité est coupé. Une capacité sans pratique est une promesse sans mécanisme. Une évaluation qui ne teste pas la capacité mesure autre chose.

---

## Les six capacités

Chacune répond aux quatre questions imposées : *quoi*, *dans quelle situation*, *à quel standard*, *comment le voit-on*.

### C1 — Prétraiter un corpus en justifiant chaque décision

| | |
|---|---|
| **Quoi** | Produire une liste de tokens à partir de textes français bruts, et nommer pour chaque étape ce qu'elle fait perdre. |
| **Situation** | On vous donne 30 avis clients non nettoyés (accents, apostrophes, majuscules, chiffres, fautes). |
| **Standard** | Le pipeline couvre normalisation, tokenisation, stop words, lemmatisation. Chaque décision est justifiée par la tâche, pas par l'habitude. Au moins deux pertes sont nommées explicitement. |
| **Comment on le voit** | Bloc 1 du TP : l'étudiant écrit `normalize()` et `tokenize()`, mesure le vocabulaire avant/après, et répond à 4 questions d'interprétation dont une sur la négation. |

**Ce qui n'est *pas* cette capacité** : « connaître la liste des stop words de NLTK ». Réciter une liste n'est pas décider.

---

### C2 — Mesurer une similarité de surface et en énoncer la cécité

| | |
|---|---|
| **Quoi** | Calculer à la main une distance de Levenshtein sur une matrice, l'interpréter comme un nombre d'opérations, et dire pourquoi elle ne dit rien du sens. |
| **Situation** | Une requête contient une faute de frappe (`salom`) ; un catalogue contient un synonyme (`automobile` pour `voiture`). |
| **Standard** | La matrice est remplie correctement (bords puis cases), la distance est lue dans la dernière case, et l'étudiant distingue les deux cas : le premier se répare, le second non. |
| **Comment on le voit** | Exercice de la section 3 : matrice `chat`/`chats` remplie sans aide + question de transfert `voiture`/`automobile`. |

**Piège visé** : croire qu'une similarité de chaînes est une similarité de sens. C'est le point de blocage n°1 de la progression.

---

### C3 — Vectoriser un document et classer une requête

| | |
|---|---|
| **Quoi** | Construire la matrice documents × termes d'un petit corpus, calculer les cosinus d'une requête, classer les documents, et expliquer un score nul. |
| **Situation** | Corpus de 4 documents, requête `le chat`, puis requête `animal de compagnie`. |
| **Standard** | Le classement est exact (D1 en tête à 0,671), le cosinus nul est expliqué par le vecteur nul de la requête — et non par « le document ne parle pas de chat ». |
| **Comment on le voit** | Bloc 2 du TP : `CountVectorizer`, classement, puis requête volontairement hors vocabulaire (OOV) qui produit un vecteur nul. |

**Ce qui n'est *pas* cette capacité** : « savoir que scikit-learn existe ». La capacité est de prédire le classement **avant** de l'exécuter.

---

### C4 — Pondérer et anticiper l'effet d'une pondération

| | |
|---|---|
| **Quoi** | Calculer un IDF avec la convention scikit-learn, puis **prédire** si TF-IDF change ou non le classement d'une requête, avec justification. |
| **Situation** | Requête `le chat` (le classement ne change pas) vs requête `félin salon` (D3 passe devant D4). |
| **Standard** | L'étudiant calcule `idf(félin) = ln(5/2)+1 = 1,916` et `idf(salon) = ln(5/4)+1 = 1,223`, puis explique l'inversion par la banalisation de `salon`, pas par « TF-IDF est meilleur ». |
| **Comment on le voit** | CFU n°2 (section 5) : quatre prédictions de classement à trancher avant le calcul. |

**Piège visé** : croire que TF-IDF « comprend » le sens. Il corrige un biais de fréquence, rien de plus.

---

### C5 — Expliquer Word2Vec et en bornant la portée

| | |
|---|---|
| **Quoi** | Expliquer l'hypothèse distributionnelle, distinguer CBOW et Skip-gram, calculer le coût en paramètres, lire une similarité, et nommer quatre limites. |
| **Situation** | Requête `félin` sur un corpus qui ne contient que `chat` ; mot `avocat` qui a deux sens. |
| **Standard** | L'hypothèse est énoncée comme une hypothèse (« des mots qui partagent leurs voisins ont souvent un sens proche »), pas comme un fait. Le coût est donné à `2 × |V| × d`. Les quatre limites sont nommées avec un exemple chacune. |
| **Comment on le voit** | Bloc 3 du TP : voisins de 3 mots, une analogie, un échec (`avocat`), comparaison avec le classement TF-IDF du bloc 2. |

**Piège visé** : prendre « proche » pour « synonyme ». Sur le modèle du TP, `chaud` et `froid` sont à 0,74.

---

### C6 — Choisir une représentation pour une situation nouvelle

| | |
|---|---|
| **Quoi** | Étant donné trois situations professionnelles, choisir une représentation, la justifier, et nommer la limite acceptée. |
| **Situation** | (a) chercher `voiture` dans un catalogue qui dit `automobile` ; (b) retrouver les documents où `avocat` est le fruit ; (c) répondre à une question dont aucun mot n'est dans le corpus. |
| **Standard** | Une représentation nommée, une justification liée à la situation, une limite acceptée explicitement. Aucune réponse « ça dépend » sans critère. |
| **Comment on le voit** | Exercice de clôture (section 8) + grille du TP. C'est la capacité de transfert : c'est elle qui décide si le cours a servi. |

**C'est la capacité terminale.** C1 à C5 sont des moyens ; C6 est la fin.

---

## Matrice capacité × preuve

| Capacité | Enseignée | Pratiquée en cours | Évaluée |
|---|---|---|---|
| C1 Prétraiter | S2 | Prédiction + fading NFC + CFU 1 | TP bloc 1 + ticket S2 |
| C2 Levenshtein | S3 | Fading matrice (4 étapes) | Exercice S3 + ticket S3 |
| C3 Vectoriser / classer | S4 | Prédiction de classement | TP bloc 2 + CFU 2 |
| C4 Pondérer | S5 | Prédiction avant calcul | TP bloc 2 + ticket S5 |
| C5 Word2Vec | S6 | Calcul de paramètres | TP bloc 3 + ticket S6 |
| C6 Choisir | S7–S8 | Les trois situations | Exercice de clôture + grille |

**Contrôle d'alignement (UbD / Biggs)** : chaque capacité a au moins une pratique en séance *et* une preuve évaluée. Aucune capacité n'est seulement exposée. Aucune évaluation ne porte sur autre chose que C1–C6.

---

## Ce qui a été retiré de la version précédente, et pourquoi

| Retiré | Raison |
|---|---|
| Objectifs en verbe vague (« comprendre », « savoir expliquer ») | On ne peut pas concevoir de pratique pour « comprendre ». Remplacés par six capacités observables. |
| La slide « Ce qu'il faut savoir refaire à la main » (6 opérations, fin de cours) | Arrivait trop tard : c'était la liste des capacités, découverte après 2 h 20. Remontée en tête de cours sous forme de contrat. |
| Les slides de correction d'exercice données d'emblée | Les réponses passent dans `answers/` ou derrière une slide de révélation explicite. Une réponse visible n'est pas une pratique. |
| Le récapitulatif « Ce qu'il faut retenir » en 5 puces | Remplacé par une carte de capacités + un ticket de sortie qui exige un rappel libre. Relire des puces n'apprend rien. |
