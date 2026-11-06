# Réponses — tickets de sortie, CFU et diagnostic

**À n'ouvrir qu'après avoir écrit sa réponse.** Une réponse lue avant la tentative ne produit aucun effet de rappel : elle donne l'impression de savoir, ce qui est le contraire du but.

---

## Diagnostic d'entrée (S0)

| # | Question | Réponse | Si faux, que réviser |
|---|---|---|---|
| 1 | Produit scalaire de `[1, 2, 3]` et `[1, 1, 1]` ? | `1+2+3 = 6`. Norme de `[1,2,3]` : `√14 ≈ 3,74` | Cours 2 — produit scalaire. Tout le cosinus de S4 en dépend. |
| 2 | En régression logistique, que vaut la sigmoïde pour un score de 0 ? | `0,5` — c'est le point d'indécision | Cours 4 — sigmoïde |
| 3 | 40 vrais positifs, 10 faux négatifs, 5 faux positifs. Rappel ? | `40 / (40+10) = 0,80` | Cours 4 — matrice de confusion |
| 4 | `fit` puis `predict` : quelle différence en une ligne ? | `fit` apprend les paramètres sur les données ; `predict` les applique à de nouvelles données | Cours 2. Important : en S4 c'est `fit`/`transform`, pas `fit`/`predict`. |
| 5 | Pourquoi standardiser une colonne avant un modèle linéaire ? | Pour ramener les colonnes à une même échelle (moyenne 0, écart-type 1), sinon une variable en euros écrase une variable en années | Cours 2 |

**Prédiction (aucune bonne réponse)** : « que fait un ordinateur quand on lui demande de comparer deux phrases ? »

On relève 3 ou 4 réponses à voix haute **sans les corriger**. Elles sont reprises en S8, où l'on demande aux mêmes étudiants de dire ce qu'ils répondraient maintenant. L'écart entre les deux est la mesure la plus honnête de ce que la séance a produit.

**Routage** : si plus de 3 étudiants sur 10 ratent l'item 1, le cosinus de S4 sera subi. Prévoir 3 minutes de rappel avant la slide « Mesurer un angle ».

---

## Ticket S1

**1.** Les quatre sources :

| Source | Exemple |
|---|---|
| Ambiguïté | `avocat` — le fruit ou le métier |
| Productivité / créativité | `googliser`, `chanmé` — mots qui n'existaient pas |
| Variabilité de surface | `été`, `ÉTÉ`, `ete` — trois écritures, un mot |
| Dépendance au contexte | `La banque était fermée` — banque de fleuve ou banque d'argent, indécidable seul |

**2.** Les **sources** décrivent ce qui rend la tâche difficile : ce sont des propriétés du langage. Les **niveaux** décrivent les étages d'analyse d'une phrase (morphologique, syntaxique, sémantique, discursif) : c'est une anatomie, pas une liste d'obstacles. Une même source de difficulté peut se manifester à plusieurs niveaux.

*Réponse insuffisante* : « les sources c'est ce qui est dur, les niveaux c'est les niveaux ». Il faut nommer qu'un niveau est un **étage de description** et une source un **mécanisme d'échec**.

---

## Ticket S2

**1.** `Les CHATS d'Emily DORMENT.`

| Étape | Résultat |
|---|---|
| Normaliser (NFC + minuscules) | `les chats d'emily dorment.` |
| Tokeniser (`\w+`) | `[les, chats, d, emily, dorment]` |
| Filtrer les tokens d'une lettre | `[les, chats, emily, dorment]` |
| Retirer les stop words | `[chats, emily, dorment]` |
| *(lemmatiser)* | `[chat, emily, dormir]` |

**2.** Trois décisions qui font perdre, au choix :

- **retirer les accents** → `côte`, `cote`, `côté` fusionnent ;
- **retirer les stop words** → `je ne veux pas payer` devient `veux payer`, le sens s'inverse ;
- **passer en minuscules** → `Orange` l'opérateur devient `orange` le fruit.

**3.** Parce qu'une méthode lexicale est **explicable** (on peut montrer pourquoi D1 sort premier), **peu coûteuse**, et qu'elle suffit quand l'utilisateur emploie les mots des documents. Elle échoue par **absence de terme**, pas par mauvais ordre : c'est mesurable, donc corrigeable ensuite. Commencer par le simple n'est pas une erreur, c'est une base de comparaison.

---

## Ticket S3

**1.** Distance **1**. Le chemin optimal : on garde `c`, `h`, `a`, `t` (quatre correspondances, coût 0) puis on **insère** `s` à la fin (coût 1). Aucune substitution n'est nécessaire.

**2.** `poisson` / `poison` : distance **1** (une suppression), et deux référents sans rapport. Autres cas : `teint` / `tain`, `vache` / `bâche`. Une distance d'édition mesure un écart d'**orthographe**, jamais un écart de sens.

**3.** `re.findall(r"\w+", "aujourd'hui")` donne `['aujourd', 'hui']` : l'apostrophe coupe le mot en deux. Conséquence : `aujourd'hui` et `aujourd` deviennent deux types distincts, et une recherche sur le mot entier ne trouve plus rien. C'est le même mécanisme que pour `l'ordinateur`.

---

## Ticket S4

**1.** Le vecteur de la requête ne contient que des **zéros** : aucun de ses mots n'a de colonne. Le cosinus vaut alors `0/0`, qui n'est **pas défini** ; scikit-learn renvoie `0` par convention. Les quatre documents sont donc à égalité, y compris ceux qui parlent du sujet.

Ce n'est pas « le document n'est pas pertinent » : c'est « la mesure n'existe pas ». La distinction est le cœur de la réponse.

**2.** Même vecteur de comptage, **cosinus = 1**. Cela prouve que le sac de mots **perd l'ordre** : deux phrases qui racontent des histoires opposées sont jugées identiques.

**3.** Deux raisons :

- le vocabulaire est **figé** par `fit` : `automobile` n'a de colonne que si le corpus la contient ; sinon le mot est ignoré et son vecteur reste vide ;
- même présents tous les deux, `voiture` et `automobile` occupent **deux colonnes distinctes**, sans recouvrement : le cosinus entre deux colonnes disjointes est 0. La lemmatisation n'aide pas — ce ne sont pas deux formes d'un même lemme.

---

## Ticket S5

**1.** `idf(t) = ln( (1+N) / (1+df(t)) ) + 1`

- le `+1` au **dénominateur** évite la division par zéro et lisse les petits corpus ;
- le `+1` **final** garantit qu'aucun terme ne descend sous un poids de 1.

**2.** **Non.** Un mot présent dans les 4 documents : `ln(5/5) + 1 = ln(1) + 1 = 1`. Avec la convention scikit-learn, l'IDF ne descend **jamais** à 0. C'est une différence avec la formule historique `log(N/df)`, qui donnerait bien 0.

C'est l'erreur la plus fréquente de la séquence. Elle vient de la formule classique, pas de celle du cours.

**3.**

| Change | Ne change pas |
|---|---|
| Tous les IDF, donc tous les poids, donc tous les cosinus | Le vocabulaire appris (sauf termes nouveaux) |
| L'ordre du classement, parfois | L'ordre des colonnes |
| La valeur de tous les scores, même pour les documents inchangés | La forme de la matrice documents × termes |

Conséquence pratique : **un IDF n'est pas portable d'un corpus à l'autre**. C'est ce que demande la question de fin de S5.

---

## Ticket S6

**1.** « Des mots qui apparaissent dans les mêmes contextes ont tendance à être employés de façon comparable. » — sans le mot « sens », parce que c'est précisément ce que l'hypothèse ne dit pas.

*Réponse insuffisante* : « des mots proches ont un sens proche ». C'est la conclusion, pas l'hypothèse.

**2.** Que **proximité vectorielle ≠ synonymie**. Deux antonymes partagent leurs contextes : `chaud` et `froid` apparaissent tous deux près de `température`, `eau`, `hiver`, `mains`. Le vecteur encode une **distribution d'emploi**, pas une direction de sens. Il faut donc cesser de lire un cosinus élevé comme « ces mots veulent dire la même chose ».

**3.** **Non.** Un mot absent du vocabulaire n'a pas de ligne dans la matrice `W` : il n'existe aucun vecteur à comparer. Les bibliothèques lèvent une erreur ou le signalent hors vocabulaire (OOV).

C'est exactement le problème que les **sous-mots** règlent (BPE, WordPiece, vus en S2) : un mot inconnu devient une suite de morceaux fréquents, donc il a toujours une représentation. Le pont avec la séance 6 est ici.

---

## Ticket S7

**1.**

| Représentation | Garde | Perd |
|---|---|---|
| Comptages | quels mots, combien de fois | l'ordre, les synonymes |
| TF-IDF | les mots qui distinguent un document | l'ordre, les synonymes, la stabilité (dépend du corpus) |
| Word2Vec | une proximité d'usage entre mots | l'ordre, les sens multiples, les mots inconnus |

**2.** La phrase confond **« score plus bas »** et **« moins pertinent »**. Le cosinus de D3 passe de 0,40 à 0,21 parce que D3 ne partage avec D1 que `le` et `sur`, deux mots présents dans les trois documents dont le poids a été réduit. Le score mesure l'appui sur des **mots discriminants** ; il ne mesure pas la pertinence. Un document peut être le plus pertinent et avoir un score faible.

**3.**

| Requête | TF-IDF change ? | Pourquoi |
|---|---|---|
| `le chat` | **Non** — D1 reste premier | `chat` est déjà discriminant (`df = 2` sur 4). Rien à corriger. |
| `félin salon` | **Oui** — D3 passe devant D4 | `salon` est banal (`df = 3`) et soutenait artificiellement D4. La pondération le banalise. |

La règle générale : **la pondération ne peut inverser un classement que si un mot banal soutenait artificiellement un document.** Elle ne crée jamais de lien entre deux colonnes différentes.

---

## CFU — rappel des bonnes réponses

| CFU | Bonne réponse | Item piège |
|---|---|---|
| 1 | **2** — minuscules, accents conservés, NFC | L'item 1 (tout aplatir) est choisi par la majorité des groupes qui confondent normaliser et simplifier |
| 2a | **2** — non, mais les écarts se creusent | L'item 1 révèle « TF-IDF comprend le sens », la conception la plus coûteuse du cours |
| 2b | **2** — D3 passe en tête | L'item 1 est le raisonnement correct **en comptages** : il montre que l'IDF n'est pas encore intégré |
