# **Exercice : Algorithme des K-means**

## **Consignes**

Dans cet exercice, nous allons appliquer l'algorithme des **K-means** sur un ensemble de données et analyser les différentes étapes du processus.

Nous répondrons aux questions en utilisant des tableaux détaillant les calculs effectués à chaque itération et en illustrant les résultats avec des graphiques.

---

## **Données initiales et définition du problème**

Nous considérons l’ensemble de données suivant :

$E = \{1, 2, 3, 10, 11, 12, 20, 21, 22\}$

Nous appliquerons l’algorithme avec **k = 3** et les centroïdes initiaux :

$\mu_1^0 = 1, \quad \mu_2^0 = 10, \quad \mu_3^0 = 22$

---

## **1. Application de l’algorithme K-means**

À chaque itération, nous calculons la distance euclidienne au carré entre chaque point et les centroïdes actuels, puis nous mettons à jour les centroïdes en prenant la moyenne des points assignés.

| Centroïdes courants | 1   | 2   | 3   | 10  | 11  | 12  | 20  | 21  | 22  | Nouveaux centroïdes                 |
| ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------------------------- |
| $\mu_1$ = 1       | ... | ... | ... | ... | ... | ... | ... | ... | ... | $\mu_1^{(i+1)} = \frac{...}{...}$ |
| $\mu_2$ = 10      | ... | ... | ... | ... | ... | ... | ... | ... | ... | $\mu_2^{(i+1)} = \frac{...}{...}$ |
| $\mu_3$ = 22      | ... | ... | ... | ... | ... | ... | ... | ... | ... | $\mu_3^{(i+1)} = \frac{...}{...}$ |

---

### **Questions :**

1. Exécuter une **itération complète** et donner :
   - Les **partitions obtenues** après l’assignation des points.
   - Les **nouveaux centroïdes** après recalcul.
   - Le barycentre des classes 
   - Une **visualisation des points et des centroïdes** dans un repère orthonormé.

2. **Combien d'itérations supplémentaires** seront nécessaires pour convergence ? Comment le définir ? 


---

## **2. Calcul de l’inertie intra-classe (WSS)**

L’inertie intra-classe est définie comme :

$$
WSS(C) = \sum_{i=1}^{k} \sum_{x \in C_i} d^2(x, \mu_i)
$$

### **Questions :**

1. Calculer **WSS** pour la partition obtenue à la question précédente.
2. Quelle valeur de **k** donnerait la meilleure partition au sens de **l’inertie intra-classe** ?

---

## **3. Calcul de l’inertie inter-classe (BSS)**

L’inertie inter-classe esrt définie comme :

$$
BSS(C) = \sum_{i=1}^{k} |C_i| d^2(\mu_i, \mu)
$$

où $|C_i|$ est le nombre d’éléments du cluster $C_i$ et $\mu$ est le centroïde global de $E$.

### **Questions :**

1. Calculer **BSS** pour la partition obtenue.
2. Quelle valeur de **k** donnerait la meilleure partition au sens de **l’inertie inter-classe** ?

---

## **4. Visualisation et analyse des résultats**

Pour mieux comprendre l’évolution des clusters, nous allons :

- **Tracer les points de l’ensemble E** en **indiquant leur appartenance aux clusters**.



