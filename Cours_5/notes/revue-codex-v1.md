# Revue critique du [plan pédagogique](</Users/christopherdeboisvilliers/Documents/dataMiningCours/Cours_5/PLAN_PEDAGOGIQUE.md>)

Le fil conducteur général est pertinent — passer du texte brut aux représentations lexicales, puis montrer leur insuffisance avant les embeddings — mais le plan n’est pas enseignable tel quel en 2 h 30. Il additionne presque un semestre d’introduction au TAL sans arbitrage assez sévère.

## Verdict par séquence

### S0 — À CORRIGER

- La frise sur cinq séances donne une direction claire et justifie correctement la place de ce cours.
- L’accroche est factuellement contradictoire : les deux phrases partagent `le` et `sur`, comme S3 le reconnaît ensuite avec un Jaccard de `2/10`. Il faut préciser « après retrait des mots-outils » ou choisir d’autres phrases.
- « Distance de Levenshtein maximale » est faux ou, au minimum, non démontré. Ce n’est d’ailleurs pas la bonne mesure pour établir la proximité sémantique de deux phrases.
- Quatre slides et cinq termes nouveaux en cinq minutes ne laissent aucune place à l’interaction. Deux slides suffiraient.

### S1 — VALIDÉ

- Bonne entrée par le problème avant les outils ; les exemples d’ambiguïté sont accessibles et les neuf minutes sont plausibles.
- Ajustement mineur : l’objectif annonce quatre sources de difficulté, mais la liste en contient au moins cinq. Les « niveaux d’analyse » ne sont pas non plus une taxonomie des difficultés ; il faut éviter de superposer les deux classifications.

### S2 — À RESTRUCTURER

- En 22 minutes, la séquence cumule Unicode, octets et points de code, NFC/NFD, sept opérations de normalisation, trois tokeniseurs, BPE/WordPiece, stop words, stemming, lemmatisation, POS et une démonstration spaCy : charge cognitive excessive.
- La progression n’est pas complètement maîtrisée : sous-mots et OOV sont évoqués avant une définition stable de vocabulaire, type, token et identifiant de token.
- Les étudiants risquent de retenir une « recette de nettoyage » universelle. Or retirer accents, ponctuation, chiffres ou stop words dépend de la tâche ; pour un Transformer ou un RAG, ces suppressions peuvent être nuisibles.
- Garder ici une chaîne minimale et comparée — texte brut, normalisation Unicode pratique, tokenisation, éventuellement lemmatisation — et reporter POS, détails Unicode et panorama des tokeniseurs.

### S3 — À RESTRUCTURER

- Les cinq distances annoncées sont correctes et la séquence montre utilement qu’une proximité orthographique n’est pas une proximité sémantique.
- Quatre slides de remplissage d’une matrice, plus récurrence, normalisation, complexité, Jaccard et six exemples en 17 minutes sont irréalistes.
- La récurrence est incomplète sans les conditions `lev(i,0)=i` et `lev(0,j)=j`. La normalisation proposée est une convention, pas « la » similarité de Levenshtein.
- Pour le parcours RAG, Levenshtein est secondaire. Garder une intuition et un cas de correction de faute ; déplacer la programmation dynamique complète et Jaccard en exercice optionnel ou annexe.

### S4 — À CORRIGER

- C’est le premier véritable noyau indispensable du cours. Le vocabulaire de 12 termes et les cosinus `0,75`, `0,50`, `≈0,267` ont été vérifiés : ils sont corrects.
- « D3 devrait être premier sur le sens » est faux pour la requête `le chat` : D1 contient exactement le chat et reste légitimement premier. Il faut une requête où la méthode lexicale échoue réellement.
- Il manque le mécanisme fondamental `fit` sur le corpus puis `transform` de la requête, ainsi que le cas d’une requête entièrement OOV donnant un vecteur nul.
- BoW, sparsité, bigrammes, norme L2, cosinus, classement manuel et limites représentent déjà une séquence dense. Elle est faisable en 26–30 minutes seulement avec un exemple unique et un calcul guidé.

### S5 — À CORRIGER

- TF-IDF est nécessaire et sa position après BoW est correcte.
- Le plan mélange deux conventions : avec `idf=ln(N/df)`, l’IDF de `chat` vaut `ln(3)≈1,10`, pas `1,69`. La valeur `1,69` vient de la formule lissée de scikit-learn.
- De même, `TfidfVectorizer` emploie par défaut un TF brut suivi d’une normalisation L2, pas exactement le TF divisé par la longueur présenté dans la formule.
- Sur les trois documents proposés, TF-IDF ne change pas l’ordre du classement ; il change les scores et l’écart entre documents. Il ne faut pas promettre un « changement de classement » sans exemple qui le produit réellement.

### S6 — À RESTRUCTURER

- Word2Vec est une bonne charnière conceptuelle, mais les prérequis sont surestimés : le cours 4 présente `βᵀx`, la sigmoïde et la BCE, pas une couche neuronale, une projection matricielle ou le softmax.
- Treize slides en 28 minutes doivent introduire one-hot, hypothèse distributionnelle, fenêtres, CBOW, Skip-gram, deux matrices, softmax, objectif d’apprentissage, cosinus dense, analogies, GloVe, fastText et biais. Ce n’est pas assimilable par ce public.
- L’exemple de fenêtre est faux : avec une fenêtre de 2, `dort` et `canapé`, séparés par trois positions, ne forment pas une paire.
- Le pont indispensable est absent : Word2Vec produit des vecteurs de **mots statiques**, pas directement des vecteurs de phrases ou de chunks. Cette distinction est cruciale pour comprendre ensuite `sentence-transformers` et le RAG.

### S7 — À RESTRUCTURER

- Treize minutes ne suffisent pas pour quatre limites, ELMo, BERT, attention, biais, RAG et `rappel@k`.
- L’exemple « s’asseoir sur la banque » transpose abusivement l’ambiguïté anglaise de *bank* : en français, on s’assoit sur un `banc`. Employer `avocat`, `vol`, `batterie` ou `glace`.
- Le « pipeline en six boîtes » énumère en réalité sept éléments et reste incomplet : la requête n’est pas encodée et le LLM/générateur ainsi que la réponse sont absents.
- Conserver les limites et un schéma RAG correctement séparé entre indexation hors ligne et interrogation en ligne. Reporter attention, chronologie ELMo/BERT et `rappel@k`.

### S8 — À CORRIGER

- La carte de synthèse et les questions flash sont pertinentes.
- Une carte mentale, cinq réponses étudiantes et l’annonce détaillée du TP ne tiennent pas en six minutes. Il faut 10 à 12 minutes, ou répartir les vérifications après S4, S5 et S6.
- « Savoir réciter » le pipeline ne constitue pas un acquis suffisant : demander plutôt de choisir une représentation et de justifier ses limites sur un cas court.

## Faisabilité temporelle et charge cognitive

Le calcul `73 slides / 145 min ≈ 1 min 59 s par slide` est exact, mais la conclusion tirée est fausse : ce rythme ne « laisse pas la place » aux questions. Les 145 minutes sont déjà affectées au contenu et il ne reste que cinq minutes pour huit transitions, la démonstration, les incidents techniques et les échanges.

| Séquence | Nouveaux blocs conceptuels approximatifs | Diagnostic |
|---|---:|---|
| S0 | 5 | Trop dense pour 5 min |
| S1 | 4–5 | Acceptable |
| S2 | >12 | Excessif |
| S3 | 6–7 | Trop élevé pour 17 min |
| S4 | 7 | Dense mais cohérent |
| S5 | 5–6 | Dense |
| S6 | >10 | Excessif |
| S7 | 7–8 | Excessif |
| S8 | 0 nouveau, 5 évalués | Évaluation trop comprimée |

La comparaison avec les 81 pages du cours 3 ne valide rien : ce cours consacre de nombreuses slides successives à une même idée et ne semble pas réserver une heure au TP. Le cours 4 utilise environ 44 slides pour un ensemble beaucoup plus homogène. Une cible réaliste serait environ 50–55 slides, 120–125 minutes planifiées et 20–30 minutes pour les calculs guidés, questions, transitions et marge.

## Faisabilité du TP d’une heure — À RESTRUCTURER

- Le plan annonce cinq exercices, mais en contient six, numérotés de 0 à 5. Le total fait exactement 60 minutes : aucune lecture de consigne, erreur de code ou transition n’est budgétée.
- Implémenter Levenshtein, effectuer une recherche, comparer une autre mesure et interpréter le tout en 12 minutes n’est réaliste qu’avec une fonction presque entièrement préremplie.
- Construire BoW, calculer un cosinus à la main, utiliser deux vectoriseurs et expliquer un changement de classement en 14 minutes est également trop ambitieux.
- Un corpus de 2 000 mots est insuffisant pour apprendre des voisins Word2Vec ou une analogie interprétables. Avec le `min_count=5` par défaut, beaucoup de mots disparaîtront ; avec `min_count=1`, les vecteurs de mots rares seront essentiellement du bruit. Le support Le Wagon emploie des milliers de phrases ou des embeddings préentraînés.
- « Aucun téléchargement obligatoire » est incompatible avec NLTK et spaCy si les ressources ne sont pas embarquées : `word_tokenize`, les stop words NLTK et `fr_core_news_sm` sont des ressources séparées. Une cellule `pip install` pendant le TP n’est pas une parade pédagogique fiable.
- `difflib.SequenceMatcher` n’implémente pas Levenshtein. La comparaison peut être intéressante, mais seulement si cette différence est explicitement enseignée.

Correction concrète : trois blocs notés — prétraitement, BoW/TF-IDF/cosinus, inspection d’embeddings préentraînés ou pré-calculés — avec 10 à 15 minutes de marge. Levenshtein peut rester optionnel ou très fortement scaffoldé. L’environnement et toutes les ressources doivent être préinstallés et testés hors ligne.

## Rapport avec les cours précédents

La continuité existe, mais elle est plus faible que le plan ne l’affirme :

- Le cours 2 fournit gradient, produit scalaire, vecteur de paramètres et pratique scikit-learn : bonne base pour le cosinus et l’idée d’apprentissage de poids.
- Le cours 4 fournit score linéaire, sigmoïde et BCE, mais pas les couches neuronales ni le softmax. S6 utilise donc un prérequis non enseigné.
- Le `rappel@k` pourrait être relié au recall du cours 4, à condition d’expliquer qu’il s’agit d’une métrique de retrieval portant sur un ensemble de documents pertinents.
- Les notions de validation et de variabilité du cours 3 pourraient servir à expliquer l’instabilité de Word2Vec sur petit corpus et la nécessité d’une évaluation, mais ce lien n’est pas exploité.
- Le cours 5 passe brutalement d’une pédagogie très progressive à plus de dix notions nouvelles en vingt minutes. La rupture principale est le rythme, pas Python.
- Le support du cours 1 n’ayant pas été fourni parmi les documents à examiner, le prérequis sur les distances ne peut être vérifié indépendamment.

## Erreurs scientifiques ou imprécisions

- Les phrases d’ouverture ont deux mots communs, pas zéro.
- Leur distance de Levenshtein n’est pas « maximale ».
- `len("é")` vaut 1 pour la forme NFC courante en Python ; c’est `len(unicodedata.normalize("NFD", "é"))` qui vaut 2.
- `[A-Za-zÀ-ÿ]+` inclut notamment `×` et `÷`, exclut `œ/Œ` et ne traite pas correctement les marques combinantes.
- La récurrence de Levenshtein est correcte, mais incomplète sans les conditions initiales.
- Les cinq valeurs de Levenshtein, le Jaccard `2/10` et les trois cosinus BoW sont corrects.
- La valeur TF-IDF `1,69` ne correspond pas à la formule non lissée affichée, qui donne `≈1,10`.
- Le TF présenté n’est pas celui utilisé par défaut par `TfidfVectorizer`.
- D3 ne devrait pas être classé devant D1 pour la requête `le chat`.
- La paire `(dort, canapé)` n’appartient pas à une fenêtre Word2Vec de taille 2.
- `10 000 × 100 = 1 000 000` est le nombre de paramètres d’une table d’embeddings. Un Word2Vec avec couche de sortie possède aussi des poids de sortie, soit approximativement une seconde matrice de cette taille.
- La formule CBOW conditionne formellement sur une liste qui inclut `w_t`. Il faut définir le contexte en excluant la cible et diviser par le nombre réel de mots de contexte.
- « La couche cachée = l’embedding » est trop sommaire : la matrice d’entrée contient les vecteurs ; l’activation cachée CBOW est l’agrégation des vecteurs du contexte.
- Les proximités Word2Vec capturent une similarité distributionnelle, pas nécessairement le « sens » : antonymes et termes thématiquement associés peuvent être proches.
- L’exemple français de polysémie de `banque` est invalide.
- Le pipeline RAG annoncé comporte sept éléments, pas six, et omet l’encodage de la requête ainsi que la génération.
- `SequenceMatcher` n’est pas une implémentation de Levenshtein.
- « Tous les cursus sérieux » suivraient exactement la progression annoncée est une généralisation contredite par les références citées elles-mêmes : Le Wagon et CS224N suivent d’autres ordres.

## Notions manquantes

### Avant le cours 6

- Distinction explicite entre **type**, **token**, identifiant de token, one-hot et vecteur d’embedding.
- Projection linéaire/multiplication matricielle et softmax minimal, ou suppression de la formule qui les utilise.
- Séquences de longueur variable, padding et masque, au moins en intuition.
- Différence entre embedding statique d’un mot, embedding contextualisé d’un token et embedding global d’une phrase.
- Agrégation/pooling : expliquer pourquoi une collection de vecteurs de mots n’est pas encore un vecteur de document.
- Effet de la taille du corpus, de `min_count`, de la graine et de la fréquence des mots sur la qualité d’un Word2Vec.

### Avant le cours 8

- Distinction document / chunk / requête / contexte fourni au LLM.
- Séparation entre phase d’indexation hors ligne et phase d’interrogation en ligne.
- Encodage des chunks et de la requête dans le même espace vectoriel.
- Différence entre retrieval et génération : le retriever ne répond pas et le LLM ne recherche pas spontanément dans l’index.
- Construction du prompt avec question et passages récupérés, puis réponse avec sources.
- Définition d’un jugement de pertinence avant toute métrique telle que `rappel@k`.

## Notions à reporter

- Détails octet/point de code et panorama NFC/NFD ; conserver seulement une démonstration pratique courte.
- POS tagging détaillé et préparation à la NER.
- Matrice complète de Levenshtein, complexité avancée et Jaccard.
- Comparaison détaillée de plusieurs stemmers/lemmatiseurs.
- Dérivation Word2Vec, softmax complet et negative sampling.
- GloVe et fastText en tant que panorama séparé.
- ELMo, histoire des embeddings contextuels et intuition de l’attention.
- `rappel@k`, MRR et protocole d’évaluation au cours 7.
- Analyse détaillée des biais au cours 6 ou 9 ; une alerte d’une phrase peut rester ici.

## Corrections prioritaires

1. **Réduire le volume à environ 50–55 slides et 120–125 minutes planifiées**, en réservant explicitement le reste aux interactions et imprévus.
2. **Recentrer le cours sur le fil utile au RAG** : tokens → BoW/TF-IDF + cosinus → limites lexicales → embeddings statiques → besoin d’embeddings de phrases contextualisés.
3. **Restructurer S6** autour de l’hypothèse distributionnelle, d’une paire d’apprentissage et de la distinction mot/phrase ; retirer la formule tant que softmax et projections ne sont pas introduits.
4. **Corriger le schéma RAG** en séparant indexation et interrogation et en ajoutant encodage de la requête, LLM et réponse.
5. **Refondre le TP** : trois blocs, dépendances préinstallées, exercices scaffoldés et embeddings préentraînés ou pré-calculés.
6. **Choisir une seule convention TF-IDF**, de préférence celle de scikit-learn puisque le TP l’utilise, et recalculer tous les exemples avec cette convention.
7. **Alléger fortement S2** ; traiter les prétraitements comme des décisions dépendantes de la tâche, pas comme une chaîne obligatoire.
8. **Réduire S3 à une démonstration courte** et déplacer la programmation dynamique complète hors du tronc obligatoire.
9. **Ajouter les maillons manquants** : vocabulaire `fit/transform`, OOV, vecteur nul, embedding de mot contre embedding de texte.
10. **Corriger et exécuter tous les exemples annoncés**, notamment l’accroche, la fenêtre Word2Vec, les paramètres, la polysémie française et les classements TF-IDF.

# Verdict global — À RESTRUCTURER

Le plan possède une architecture intellectuelle prometteuse et plusieurs calculs justes, mais il n’est ni temporellement faisable ni suffisamment stabilisé scientifiquement. Les défauts les plus graves sont la surcharge de S2, S6 et S7, le faux pont entre Word2Vec et les embeddings de chunks, le pipeline RAG incomplet et un TP dont les résultats Word2Vec seraient pédagogiquement trompeurs. Une simple réduction cosmétique des slides ne suffira pas : il faut arbitrer les objectifs.