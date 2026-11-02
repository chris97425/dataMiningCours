# Revue critique — Bloc 1

**Verdict immédiat : À CORRIGER.** La structure est fidèle au plan et la réalisation visuelle est propre, mais les slides 3 et 6 contiennent des erreurs qui touchent directement les notions fondamentales du cours.

Références examinées : plan validé S0–S1 :codex-file-citation{path="/Users/christopherdeboisvilliers/Documents/dataMiningCours/Cours_5/PLAN_PEDAGOGIQUE.md" purpose="source"}, source des six slides :codex-file-citation{path="/Users/christopherdeboisvilliers/Documents/dataMiningCours/Cours_5/presentation.md" purpose="source"}, repères stylistiques des cours précédents :codex-file-citation{path="/Users/christopherdeboisvilliers/Documents/dataMiningCours/Cours_2/presentation.md" purpose="source"} :codex-file-citation{path="/Users/christopherdeboisvilliers/Documents/dataMiningCours/Cours_3/presentation.md" purpose="source"} :codex-file-citation{path="/Users/christopherdeboisvilliers/Documents/dataMiningCours/Cours_4/presentation.md" purpose="source"}.

## Verdict par slide

| Slide | Verdict | Évaluation |
|---|---|---|
| **1 — Titre** | **VALIDÉ** | Couverture sobre, lisible et cohérente avec les cours 2 à 4 : même titre générique, auteur, date, thème et format. Le sous-titre précise utilement le contenu. Beaucoup d’espace vide, mais acceptable pour une page de titre. |
| **2 — Plan de la séance** | **VALIDÉ** | Bonne fidélité à S0 : progression du cours, position dans les cinq séances et durée cours/TP sont explicites. Hiérarchie claire, sans débordement. La colonne droite est un peu petite pour une projection lointaine. « Plan de la séance » en `###` rompt légèrement avec le `# Plan du cours` des cours 2 à 4, sans nuire réellement. |
| **3 — Deux phrases, une même scène** | **À CORRIGER** | Excellente accroche et bonne progression pour un débutant, mais le comptage mélange implicitement *tokens* et *types*. Le surlignage ne matérialise pas correctement les deux mots communs. « Rien à voir » est faux pour une méthode lexicale brute. Visuellement, la slide est claire et bien respirée. |
| **4 — Pourquoi est-ce si difficile ?** | **À CORRIGER** | Les quatre causes correspondent exactement au plan et sont bien distinguées. La grille 2×2 est équilibrée et lisible. En revanche, l’exemple `ÉTÉ / été / ete / etté` est mal qualifié : sans convention explicite de suppression des accents, il n’y a pas « une faute » mais deux graphies non standard. Les exemples de productivité illustrent surtout la variation lexicale et l’argot, moins nettement la capacité à produire des phrases inédites. |
| **5 — Quatre niveaux d’analyse** | **À CORRIGER** | La distinction entre difficultés et niveaux d’analyse est pédagogiquement très bonne et fidèle à S1. Mais les quatre niveaux sont présentés comme une taxonomie générale alors qu’il s’agit d’une sélection : la pragmatique, notamment, manque. L’exemple discursif n’affiche pas l’antécédent nécessaire. La phrase sur les Transformers est excessivement catégorique. Les textes secondaires du SVG sont trop petits pour un amphithéâtre. |
| **6 — La chaîne que nous allons construire** | **À CORRIGER** | Bonne intention de synthèse et transition logique vers S2, mais le diagramme enseigne une causalité incorrecte : la similarité cosinus ne produit ni le sens ni le contexte. Le contexte intervient dans la représentation ; la similarité produit un score ou un classement. La petite légende annonce « cinq briques aujourd’hui », alors que le bloc inférieur n’en attribue que quatre à la séance. Plusieurs libellés sont trop petits. |

Aucun débordement, chevauchement ou texte coupé n’est visible sur le montage. La cohérence formelle avec les cours 2 à 4 est forte : thème, format 4:3, couverture, bandeaux, pied de page, exemples avant formalisation et ton direct. La composition en cartes et SVG constitue toutefois une rupture stylistique sensible avec les supports antérieurs, plus proches de listes et de formules.

## Erreurs factuelles

- **Slide 3 :** les deux phrases contiennent **13 occurrences de mots**, et non 10. On obtient **10 types après passage en minuscules**. Cette distinction est cruciale juste avant l’enseignement de *type/token*.
- **Slide 3 :** seules les occurrences de `sur` sont surlignées dans les deux phrases. Le mot commun `le` n’est pas signalé de manière cohérente.
- **Slide 3 :** une représentation lexicale brute ne conclut pas « rien à voir » : `le` et `sur` donnent une intersection et une similarité non nulles. Le chevauchement devient nul seulement pour les mots porteurs de sens, ou après retrait des mots outils.
- **Slide 4 :** en français standard, `ete` et `etté` sont deux graphies fautives. `ete` ne devient une simple variante que si l’on annonce explicitement une normalisation supprimant les diacritiques.
- **Slide 6 :** le cosinus ne transforme pas une représentation en « sens/contexte ». Il compare deux vecteurs et fournit un score ; le contexte doit être encodé en amont par le modèle de représentation.

## Corrections classées par impact

1. **Critique — Corriger la logique de la slide 6.** Le schéma doit séparer représentation contextuelle, calcul de similarité et résultat de recherche. Dans son état actuel, il installe un modèle mental faux qui contaminera les cours 6 à 8.

2. **Élevé — Corriger le comptage et le surlignage de la slide 3.** Distinguer explicitement occurrences et formes distinctes, puis surligner toutes les occurrences réellement communes selon la convention choisie.

3. **Élevé — Nuancer la conclusion lexicale de la slide 3.** Distinguer faible similarité lexicale, absence de mots de contenu communs et similarité sémantique forte.

4. **Moyen — Sécuriser les formulations linguistiques des slides 4 et 5.** Clarifier le statut de `ete`, présenter les quatre niveaux comme ceux retenus dans le cours, fournir un antécédent à l’exemple discursif et supprimer la généralisation sur ce que les Transformers « mélangent ».

5. **Moyen — Augmenter la lisibilité des SVG des slides 5 et 6.** Les libellés de 13–14 px et les légendes grisées sont trop petits pour une projection ; simplifier avant d’agrandir plutôt que conserver toute la microcopie.

## Verdict du bloc

# **À CORRIGER**

La progression et l’architecture ne nécessitent pas de restructuration. En revanche, le bloc ne doit pas être enseigné en l’état : les erreurs des slides 3 et 6 portent précisément sur la distinction lexical/sémantique et sur le rôle des représentations, qui sont les deux idées fondatrices du cours.