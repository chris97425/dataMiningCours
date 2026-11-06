# Tickets de sortie et vérifications de compréhension

**Document du professeur.** Les réponses ne sont pas ici : elles sont dans `answers/tickets-et-cfu.md`, à ouvrir seulement après la tentative.
**Méthode** : items de rappel (`retrieval-practice-generator`, Roediger & Butler 2011, Karpicke & Roediger 2008) ; CFU à distracteurs diagnostiques (`k12-check-for-understanding`, Anthropic × Learning Commons).

---

## Comment s'en servir

| | |
|---|---|
| **Un ticket de sortie** | 2 à 3 questions, 90 secondes, à l'écrit sur papier libre. Une question porte sur la section qui vient de finir, **au moins une** sur une section antérieure. Ramassé ou non — l'effet vient de l'effort de rappel, pas de la note. |
| **Une CFU** | 1 à 3 items à choix, lus à voix haute, réponse par main levée ou par carton. **On ne note pas.** On lit ce que la réponse révèle, et on route. |
| **Règle commune** | L'étudiant écrit ou dit sa réponse **avant** de voir les options quand c'est possible. Choisir n'est pas se rappeler. |

### Distribution des types de rappel

Le rappel libre produit l'effet le plus fort et c'est le plus dur ; la reconnaissance est la plus faible. Les tickets sont donc majoritairement en **rappel libre et rappel indicé**, la reconnaissance étant réservée aux CFU (où le but est de révéler une conception fausse, pas de produire de la rétention).

| Type | Tickets | CFU |
|---|---|---|
| Rappel libre (aucun indice) | 11 items | — |
| Rappel indicé (amorce partielle) | 7 items | — |
| Reconnaissance (options) | 1 item | 6 items |

---

## CFU 1 — Section 2 · Normalisation

**Quand** : après la slide « Normaliser, c'est choisir ce qu'on perd », avant de passer à la tokenisation.
**Durée** : 90 secondes. **Réponse** : main levée par option, ou doigts 1-2-3-4.

> Vous analysez **2 000 avis clients** en français pour en extraire les thèmes. Quel choix de normalisation est le plus défendable ?
>
> **1.** Passer en minuscules et retirer tous les accents, pour que `Café`, `cafe` et `CAFÉ` se rejoignent.
> **2.** Passer en minuscules, garder les accents, et ramener toutes les chaînes en NFC.
> **3.** Retirer d'abord les stop words, dont `ne` et `pas`, puis normaliser le reste.
> **4.** Ne rien normaliser : le tokenizer du modèle s'en charge.

**Ce que chaque réponse révèle, et quoi faire ensuite**

| Rép. | Conception sous-jacente | Ce que ça coûte ici | Prochain geste |
|---|---|---|---|
| **1** | « Normaliser, c'est tout aplatir » — l'accent est traité comme du bruit | `côte`, `cote`, `côté` fusionnent ; sur des avis, `déçu` et `décu` se rejoignent (utile) mais `tâche` et `tache` aussi (coûteux) | Revenir au tableau « ce qu'on perd ». Demander de citer **deux collisions** que ce choix crée dans un vocabulaire d'hôtellerie. |
| **2** | Correct | — | Enchaîner sur la tokenisation. |
| **3** | Confusion d'ordre : les stop words sont traités comme une étape de normalisation | La négation disparaît avant qu'on ait décidé de la garder ; impossible de revenir en arrière | Aller à la slide « Stop words : ce qu'on gagne, ce qu'on risque ». Faire dire à voix haute ce que devient `je ne veux pas payer`. |
| **4** | Vrai pour un modèle préentraîné, faux pour l'outil de cette séance | `CountVectorizer` ne normalise rien : `Chat` et `chat` resteront deux colonnes | Poser la question de tri : « quel objet lit vos textes, ici ? » Faire nommer la différence entre un tokenizer BERT et `CountVectorizer`. |

**Seuil d'alerte** : si plus de 30 % du groupe choisit 1 ou 3, la section 2 doit être reprise à l'oral avant la suite — la tokenisation s'appuiera sur une base fausse.

---

## CFU 2a — Section 5 · Prédiction avant calcul (`le chat`)

**Quand** : après la slide « Tous les mots ne se valent pas », **avant** d'afficher la formule de l'IDF.
**Durée** : 60 secondes. **Consigne** : réponse écrite, une ligne de justification, **avant** de voir les options. Puis on révèle les options.

> Requête `le chat` sur les quatre documents. On passe des comptages au TF-IDF. **L'ordre du classement change-t-il ?**

*(On ne montre les options qu'après que chacun a écrit sa phrase.)*

> **1.** Oui — D3 remonte, puisque TF-IDF rapproche les mots rares et que `félin` est rare.
> **2.** Non — mais les écarts entre les documents se creusent.
> **3.** Oui — D4 remonte, parce que TF-IDF récompense les documents qui répètent un mot.
> **4.** Non — et les scores restent identiques, puisque les vecteurs sont normalisés.

**Ce que chaque réponse révèle**

| Rép. | Conception sous-jacente | Ce que ça coûte | Prochain geste |
|---|---|---|---|
| **1** | **La plus fréquente et la plus coûteuse** : « TF-IDF comprend le sens » | On attend d'une pondération qu'elle règle un problème de vocabulaire. L'étudiant sera déçu en production, puis accusera l'outil. | Ne pas corriger tout de suite. Faire constater que D3 vaut 0 **parce que la colonne `félin` et la colonne `chat` sont deux colonnes différentes**. Une pondération multiplie des colonnes, elle n'en crée pas. |
| **2** | Correct | — | Enchaîner sur la révélation, puis CFU 2b. |
| **3** | Confusion entre « répéter » et « être rare » : les deux signaux sont inversés | Mène à sur-pondérer les documents longs et répétitifs | Montrer que D4 **baisse** (0,365 → 0,214), pas monte. La répétition est déjà dans le TF ; l'IDF la contredit. |
| **4** | Confusion sur la normalisation L2 : on croit qu'elle annule toute pondération | Empêche de comprendre pourquoi les écarts changent | Poser : « l'IDF est-il le même pour tous les termes ? » Si non, ce n'est pas un facteur global, donc L2 ne l'annule pas. |

---

## CFU 2b — Section 5 · Prédiction avant calcul (`félin salon`)

**Quand** : juste après la révélation de la CFU 2a. C'est le moment pédagogique de la séquence.
**Durée** : 60 secondes.

> Nouvelle requête : `félin salon`. Qui arrive en tête, cette fois en TF-IDF ?

> **1.** D4 — il répète `salon` deux fois.
> **2.** D3 — `félin` est rare, donc lourd.
> **3.** D1 — c'est le document le plus court, il est donc avantagé.
> **4.** D1 et D2 à égalité, et devant.

**Ce que chaque réponse révèle**

| Rép. | Conception | Prochain geste |
|---|---|---|
| **1** | C'est le raisonnement **correct en comptages** (D4 gagne bien à 0,365) — l'étudiant n'a pas encore intégré que l'IDF banalise `salon` | Faire calculer `idf(salon) = 1,223` contre `idf(félin) = 1,916`, puis montrer l'inversion sur le graphique. |
| **2** | Correct | Faire formuler **pourquoi** : `salon` est dans 3 documents sur 4. C'est le seul cas du cours où la pondération corrige un classement réellement faux. |
| **3** | Confusion : le cosinus ignore la longueur, donc la brièveté n'avantage pas — mais elle ne pénalise pas non plus | Revenir à la slide cosinus vs distance euclidienne. |
| **4** | Confusion sur la normalisation L2 : on croit qu'elle écrase les scores | Montrer les valeurs : D1 = D2 = 0,144, mais **D3 = 0,291**. |

**Pourquoi cette CFU est la plus importante du cours** : elle sépare les étudiants qui ont compris « pondérer » de ceux qui ont compris « TF-IDF est mieux ». Le second groupe est majoritaire et il est dangereux en production.

---

## Tickets de sortie

Format : 90 secondes, à l'écrit, sans notes. Les réponses sont dans `answers/tickets-et-cfu.md`.

### Ticket S1 — après « Quatre niveaux d'analyse »

1. *(rappel libre)* Citez les **quatre** sources de difficulté du langage traitées ici, avec un exemple différent de ceux de la slide pour chacune.
2. *(rappel indicé)* Les niveaux d'analyse et les sources de difficulté sont deux classifications **différentes**. Dites en une phrase ce qui les distingue.

**Ce que ça teste** : la liste close de 4 (et non 5), et la non-confusion avec les niveaux.

---

### Ticket S2 — après « La chaîne complète »

1. *(rappel libre)* Vous recevez `Les CHATS d'Emily DORMENT.` Décrivez les quatre étapes de prétraitement dans l'ordre, et donnez le résultat de chacune.
2. *(rappel libre)* Nommez **une** décision de prétraitement qui fait perdre de l'information, et dites ce qu'elle fait perdre.
3. *(rappel indicé, section 1)* Pourquoi commence-t-on par compter des mots alors qu'on vient de montrer que cela ne marche pas sur les synonymes ?

**Ce que ça teste** : C1 en exécution ; la conscience de la perte ; le rappel de la justification donnée en S1.

---

### Ticket S3 — après « Où ça marche, où ça casse »

1. *(rappel libre)* `chat` → `chats` : quelle est la distance de Levenshtein, et quelle opération correspond au chemin optimal ?
2. *(rappel libre)* Donnez un cas où une distance d'édition **petite** ne signifie pas que les deux mots sont proches par le sens.
3. *(rappel indicé, section 2)* Vous devez nettoyer `aujourd'hui`. Dites ce que produit un découpage sur `\w+`, et pourquoi c'est un problème.

**Ce que ça teste** : C2 (calcul + cécité sémantique) ; le rappel de la tokenisation, qui sera réutilisé en S4.

---

### Ticket S4 — après « Et si aucun mot de la requête n'est connu ? »

1. *(rappel libre)* Une requête n'a **aucun** mot du vocabulaire. Que vaut son vecteur, et que renvoie le cosinus ? Pourquoi ?
2. *(rappel indicé)* `le chien mord l'homme` et `l'homme mord le chien` : même vecteur de comptage, cosinus = ? Que cela prouve-t-il ?
3. *(rappel libre, sections 2 et 3)* Deux raisons pour lesquelles `voiture` et `automobile` obtiennent un cosinus de 0 ici.

**Ce que ça teste** : C3, y compris le cas dégénéré 0/0 ; la limite d'ordre ; l'articulation avec S2 (stop words) et S3 (Levenshtein ne sait rien du sens).

---

### Ticket S5 — après « Ce que TF-IDF ne sait pas faire »

1. *(rappel libre)* Écrivez la formule de l'IDF utilisée par scikit-learn, et expliquez le rôle du `+1` au dénominateur.
2. *(rappel libre)* Un mot apparaît dans **tous** les documents. Son IDF sklearn vaut-il 0 ? Justifiez par le calcul.
3. *(rappel indicé, section 4)* Vous ajoutez 100 documents au corpus. Qu'est-ce qui change dans les scores TF-IDF, et qu'est-ce qui ne change pas ?

**Ce que ça teste** : C4 (formule + non-annulation) ; la dépendance au corpus ; le rappel de S4.

*Point de vigilance* : la question 2 est celle où l'erreur « IDF = 0 quand le mot est partout » apparaît le plus souvent. La réponse est `ln(5/4)+1 = 1,223`, jamais 0.

---

### Ticket S6 — après « Les analogies, et où elles échouent »

1. *(rappel libre)* Énoncez l'hypothèse distributionnelle en une phrase, sans utiliser le mot « sens ».
2. *(rappel libre)* `chaud` et `froid` ont un cosinus de 0,74 sur le modèle du TP. Qu'est-ce que cela vous oblige à corriger dans ce que vous croyiez ?
3. *(rappel indicé, section 4)* Vous avez un mot nouveau, absent du vocabulaire de Word2Vec. Le cosinus peut-il le représenter ? Reliez à ce que vous avez vu en S2.

**Ce que ça teste** : C5, et précisément la limite que la v2.2 traitait trop vite (proximité ≠ synonymie) ; le pont vers les sous-mots.

---

### Ticket S7 — après « Comparer les représentations »

1. *(rappel libre)* Pour chacune des trois représentations du cours, donnez **une** chose qu'elle garde et **une** chose qu'elle perd.
2. *(rappel libre)* On vous dit : « le cosinus de D3 baisse de 0,40 à 0,21 quand on passe en TF-IDF, donc D3 est moins pertinent ». Corrigez cette phrase en une ou deux lignes.
3. *(rappel indicé, section 5)* Requête `le chat`, puis requête `félin salon` : dans lequel des deux cas TF-IDF change réellement le classement, et pourquoi l'autre non ?

**Ce que ça teste** : C6 en formation ; la lecture correcte d'une baisse de score (elle ne veut pas dire « moins pertinent », elle veut dire « moins soutenu par des mots discriminants ») ; le rappel du seul cas d'inversion.

---

## Ce qui n'est **pas** demandé, et pourquoi

| Écarté | Raison |
|---|---|
| QCM de définition en fin de cours | La reconnaissance ne produit presque pas de rétention. Les définitions utiles sont testées en rappel libre dans les tickets. |
| « Récitez les cinq limites » | On demande une limite **avec un exemple**, jamais une liste. Une liste récitée ne se transfère pas. |
| Questions dont la réponse est dans le titre de la slide | Elles mesurent la lecture, pas la mémoire. |
| Plus de 3 items par ticket | Au-delà, la qualité de l'écrit chute et le temps déborde sur la section suivante. |
