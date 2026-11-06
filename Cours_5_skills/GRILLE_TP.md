# Grille d'évaluation du TP — cours 5

**Méthode** : `criterion-referenced-rubric-generator` (Brookhart 2013, Sadler 1989, Andrade 2000/2013, Jonsson & Svingby 2007).
**Règle de rédaction** : chaque niveau décrit **ce qui est présent dans le travail**, jamais à quel point c'est bon. Aucun mot évaluateur (excellent, bon, satisfaisant, faible, limité) : ils n'informent pas l'étudiant sur ce qu'il doit faire.

**Niveau visé** : **Autonome** sur les quatre critères. C'est le niveau qui permet de suivre la séance 6 sans rattrapage.

---

## Les quatre critères

Ils sont **indépendants** : un étudiant peut être Autonome sur le critère 1 et En construction sur le critère 4. Si deux critères produisent toujours la même note, c'est qu'ils mesurent la même chose et l'un des deux doit disparaître.

| # | Critère | Capacité | Ce qu'il isole |
|---|---|---|---|
| 1 | Prétraitement justifié | C1 | Le lien entre une décision et son effet mesuré |
| 2 | Lecture d'un classement | C3, C4 | La capacité à dire **pourquoi** un document sort devant, y compris quand le score est nul |
| 3 | Interprétation d'un vecteur dense | C5 | La distinction entre proximité d'usage et synonymie |
| 4 | Limite nommée | C6 | La capacité à dire ce qu'on accepte de perdre |

---

## Grille descriptible — version professeur

### Critère 1 — Prétraitement justifié

| Niveau | Ce qui est présent dans le travail |
|---|---|
| **Point de départ** | Le code de `normalize()` ou `tokenize()` est incomplet ou non exécutable. Les mots sont transformés sans qu'aucune décision ne soit nommée. |
| **En construction** | Le code s'exécute et produit les tokens attendus. Les décisions sont nommées (« j'ai retiré les accents ») mais aucune n'est reliée à la tâche ni à une perte. |
| **Autonome** | Le code s'exécute. Chaque étape est reliée à son effet **mesuré** sur le vocabulaire (nombre de types avant / après). Au moins une perte est nommée avec un exemple concret du corpus. |
| **Transférable** | Tout ce qui précède, plus : l'étudiant identifie une décision qui **serait différente** sur un autre corpus (avis clients vs catalogue), et explique sur quel critère il trancherait. |

### Critère 2 — Lecture d'un classement

| Niveau | Ce qui est présent dans le travail |
|---|---|
| **Point de départ** | Les scores sont calculés mais le classement n'est pas interprété, ou il est interprété en termes de « meilleur / moins bon document ». |
| **En construction** | Le classement est expliqué par les mots partagés (« D1 sort premier parce qu'il contient `chat` »). Le cas du vecteur nul est traité comme un score de 0 ordinaire. |
| **Autonome** | Chaque position est expliquée par la présence ou l'absence de **mots discriminants**, et le vecteur nul est identifié comme un cas où la mesure n'existe pas (0/0), distinct d'un score de 0. |
| **Transférable** | Tout ce qui précède, plus : l'étudiant prédit un classement **avant** de l'exécuter, et l'écart entre sa prédiction et le résultat est documenté. |

### Critère 3 — Interprétation d'un vecteur dense

| Niveau | Ce qui est présent dans le travail |
|---|---|
| **Point de départ** | Les voisins sont listés sans commentaire, ou commentés comme des synonymes (« `chat` est proche de `félin`, ils veulent dire la même chose »). |
| **En construction** | Les voisins sont lus comme « employés dans des contextes proches ». Un cas d'échec est mentionné mais non expliqué. |
| **Autonome** | Les voisins sont lus comme une proximité d'**usage**, et un cas d'échec est expliqué par un mécanisme précis (polysémie de `avocat`, ou antonymie de `chaud`/`froid`). |
| **Transférable** | Tout ce qui précède, plus : l'étudiant indique une situation où il **refuserait** d'utiliser ces vecteurs, avec la raison. |

### Critère 4 — Limite nommée

| Niveau | Ce qui est présent dans le travail |
|---|---|
| **Point de départ** | Aucune limite nommée. Le TP se termine sur les résultats numériques. |
| **En construction** | Une limite est nommée en termes généraux (« ça ne marche pas toujours ») sans exemple ni conséquence. |
| **Autonome** | Au moins une limite est nommée **avec un exemple du corpus du TP** et la conséquence pratique pour la recherche concernée. |
| **Transférable** | Tout ce qui précède, plus : la limite est reliée à la séance suivante (sous-mots, encodeur de phrases) ou à une décision de production (choisir un autre index, ajouter un correcteur). |

---

## Version étudiant

Écrite à la seconde personne, pour être lue **avant** le TP.

### Ce qu'on regardera dans votre travail

**1. Vos choix de prétraitement, et ce que vous en dites**
- Vous écrivez le code demandé, et il s'exécute.
- Pour chaque étape, vous dites ce qu'elle a changé dans le nombre de mots du vocabulaire.
- Vous citez au moins une chose que votre nettoyage a fait perdre, avec un exemple pris dans le corpus.
- *(Pour aller plus loin)* Vous dites quelle décision vous changeriez sur un autre type de corpus, et pourquoi.

**2. Votre lecture du classement**
- Vous expliquez pourquoi chaque document arrive à sa place, en parlant des mots qu'il partage avec la requête.
- Vous distinguez « ce document a un score de 0 » de « le score n'existe pas ». Vous savez dire laquelle des deux situations produit une requête hors vocabulaire.
- *(Pour aller plus loin)* Vous écrivez votre prédiction du classement **avant** de lancer le code, puis vous notez l'écart.

**3. Votre lecture des vecteurs de mots**
- Vous lisez les voisins comme « ces mots s'emploient dans des contextes proches », pas comme « ces mots veulent dire la même chose ».
- Vous prenez un cas où le modèle se trompe, et vous expliquez **pourquoi** il se trompe.
- *(Pour aller plus loin)* Vous nommez une situation où vous n'utiliseriez pas ces vecteurs.

**4. La limite que vous acceptez**
- Vous nommez au moins une limite de la méthode que vous avez utilisée.
- Vous l'illustrez avec un exemple de **votre** corpus, pas de la slide.
- Vous dites ce que cette limite change concrètement pour la recherche que vous construisez.
- *(Pour aller plus loin)* Vous reliez cette limite à ce qui vient ensuite (sous-mots, encodeur de phrases) ou à une décision technique.

---

## Barème de validation

| Critère | Autonome | En construction | Point de départ |
|---|---|---|---|
| 1 Prétraitement | obligatoire | — | — |
| 2 Classement | obligatoire | — | — |
| 3 Vecteurs denses | obligatoire | toléré si le cas d'échec est nommé | — |
| 4 Limite | obligatoire | — | — |

**Le TP est validé** quand les critères 1, 2 et 4 sont au niveau Autonome et le critère 3 au moins En construction. Ce n'est pas une note : c'est un **seuil de passage** vers la séance 6, qui suppose les quatre capacités disponibles.

**Que faire en cas de « Point de départ »** : la reprise n'est pas un nouveau TP. C'est une seule tâche ciblée — pour le critère 1, refaire `normalize()` sur trois phrases et nommer deux pertes ; pour le critère 2, expliquer trois classements dont un avec vecteur nul ; pour le critère 4, nommer une limite avec un exemple du corpus.

---

## Ce que la grille ne fait pas

- Elle ne note pas la **qualité du code** : ce n'est pas un cours de génie logiciel. Un code lisible et faux est faux.
- Elle ne récompense pas la **longueur** : une limite nommée en une ligne juste vaut mieux que trois paragraphes généraux.
- Elle ne compare pas les étudiants entre eux : chaque critère se lit contre sa propre description, pas contre le voisin.
