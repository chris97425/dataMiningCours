1️⃣ $a(i)$ = Cohésion intra-cluster

Définition : C’est la distance moyenne entre i et toutes les autres données de son propre cluster.

$a(i) = \frac{1}{|C_i|-1} \sum_{j \in C_i, j \neq i} d(i, j)$

    •	$C_i$ est l’ensemble des points du cluster de i.
	•	|C_i| est le nombre de points dans ce cluster.
	•	d(i, j) est la distance entre i et j.
	•	Plus a(i) est petit, plus i est proche des autres points de son cluster → bonne cohésion.

⸻

2️⃣ b(i) = Séparation inter-cluster

Définition : C’est la distance moyenne entre i et toutes les données du cluster voisin le plus proche.

$b(i) = \min_{C_k \neq C_i} \frac{1}{|C_k|} \sum_{j \in C_k} d(i, j)$

	•	On calcule la distance moyenne de i à chaque autre cluster, puis on choisit la plus petite.
	•	Plus b(i) est grand, plus i est éloigné du cluster voisin → bonne séparation.

📌 Comment $b(i)$ détermine le cluster le plus proche ?

Le $b(i)$ d’un point i représente la distance moyenne entre i et toutes les données du cluster voisin le plus proche.

⸻

1️⃣ Étapes pour calculer $b(i)$

Pour un point donné i appartenant à un cluster C_i :
	1.	Calculer la distance moyenne de i à chaque cluster voisin C_k (où C_k \neq C_i).
	2.	Prendre le cluster avec la plus petite distance moyenne → c’est le cluster voisin le plus proche.

$b(i) = \min_{C_k \neq C_i} \frac{1}{|C_k|} \sum_{j \in C_k} d(i, j)$

⸻

2️⃣ Exemple concret avec 6 points et 2 clusters

Imaginons ces deux clusters après application de K-Means :
	•	Cluster 1 (rouge) : P_1 = (1,2), P_2 = (2,3), P_3 = (3,2)
	•	Cluster 2 (bleu) : P_4 = (8,7), P_5 = (9,8), P_6 = (8,9)

Calcul de $b(i)$ pour P_3 = (3,2)
	•	P_3 appartient au Cluster 1.
	•	Calcul de la distance moyenne entre P_3 et tous les points du Cluster 2 :

$b(P_3) = \frac{d(P_3, P_4) + d(P_3, P_5) + d(P_3, P_6)}{3}
= \frac{\sqrt{(3-8)^2 + (2-7)^2} + \sqrt{(3-9)^2 + (2-8)^2} + \sqrt{(3-8)^2 + (2-9)^2}}{3}
= \frac{\sqrt{25+25} + \sqrt{36+36} + \sqrt{25+49}}{3}
= \frac{7.07 + 8.49 + 8.66}{3} = 8.07$

💡 Le cluster 2 étant le plus proche, b(i) prend cette valeur.

⸻

3️⃣ Interprétation
	•	Petit b(i) → Le cluster voisin est proche → Le point est mal séparé.
	•	Grand b(i) → Le cluster voisin est éloigné → Le point est bien séparé.

💡 Le score de silhouette s(i) sera élevé si $b(i)$ $\gg$ $a(i)$, ce qui signifie une bonne séparation des clusters.