🎲 Variable aléatoire : lancer d’un dé

La variable $X$ prend les valeurs possibles de ${1, 2, 3, 4, 5, 6}$, toutes avec la même probabilité :
$\mathbb{P}(X = x_k) = \frac{1}{6} \quad \text{pour } x_k \in \{1,2,3,4,5,6\}$

⸻

🧠 1. Calcul de l’espérance (moyenne)

$\mathbb{E}[X] = \sum_{k=1}^{6} x_k \cdot \mathbb{P}(X = x_k)
= \frac{1 + 2 + 3 + 4 + 5 + 6}{6} = \frac{21}{6} = 3.5$

⸻

📐 2. Calcul de la variance

La formule :

$\text{Var}(X) = \mathbb{E}[(X - \mathbb{E}[X])^2] = \sum_{k=1}^6 (x_k - 3.5)^2 \cdot \frac{1}{6}$

On calcule chaque carré des écarts à la moyenne :

$(1 - 3.5)^2 = 6.25\\
(2 - 3.5)^2 = 2.25 \\
(3 - 3.5)^2 = 0.25 \\
(4 - 3.5)^2 = 0.25 \\
(5 - 3.5)^2 = 2.25 \\
(6 - 3.5)^2 = 6.25$

Ensuite on fait la moyenne :

$\text{Var}(X) = \frac{6.25 + 2.25 + 0.25 + 0.25 + 2.25 + 6.25}{6} = \frac{17.5}{6} = \frac{35}{12}$

⸻

✅ Conclusion

La variance d’un lancer de dé équilibré à 6 faces est :
$\text{Var}(X) = \frac{35}{12} \approx 2.92$s