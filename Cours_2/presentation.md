---
marp: true
theme: neobeam
paginate: true
size: 4:3
math: mathjax
header: Cours Esiroi 2025
footer: Data mining - Christopher de Boisvilliers
title: Marp custom themes
---

<!-- _class: title -->

# Le Data Mining

<br/>

Christopher de Boisvillierrs

2025-03-17


------
<!-- header: ⭐️ Plan du cours -->

# Plan du cours
1. La régression linéaire **alias** prédire un nombre 
2. La régression logistique **alias** prédire une classe
3. Quelques notions (---- à completer ----)
---
<!-- header: 📈 La Régression linéaire -->

# 1. La régression linéaire
### **Carte d'identité de l'algorithme**

- **Nom**: Régression linéaire  
- **Type d'algorithme**: Modèle supervisé  
- **Besoin de données cibles**: Oui, des valeurs numériques continues  
- **Mission**: Trouver la meilleure droite/plan qui **minimise <span style="color:red">l'erreur</span>** entre les **<span style="color:red">prédictions</span>** et les **<span style="color:red">valeurs réels</span>**  
- **Utilité**: Prédire une valeur numérique continue (**ex: slide suivante**)  



---
### **Rappel**

Un modèle **supervisé** à besoin de données cible un $y= y_{train}+ y_{test}$  
#### **Dataset d'exemple: Prix des maisons**

| ID | Surface (m²)  &#127968; | Chambres &#128716; | Prix (€)  alias <span style="color:black">y</span>|
|----|----------------|-------------|------------|
| 1  | 85             | 2           | 210,000    |
| 2  | 120            | 3           | 310,000    |
| 3  | 65             | 1           | 175,000    |

### Question &#128269;
Qui peut m'expliquer cette phrase:
- Qui minimise  **<span style="color:red">l'erreur</span>**  entre les **<span style="color:red">prédictions</span>** et les **<span style="color:red">valeurs réels</span>** 

---

### **Une régression linéaire visuellement ressemble à cela**

<div style="display: flex; justify-content: center; align-items: center;">
  <img width="300" height="300" src="images/reg2d.png">
  <img width="350" height="350" src="images/reg3d.png">
</div>

### Question &#128269;
Sur les deux graphiques ci-dessus, qu'est que ma **régression linéaire** ? **Ma prédiction** ? **Mon erreur** ? 


---

### **La régression linéaire n'est finalement qu'une simple droite/plan**

Cela implique qu'elle est représenté mathématiquement par une formule très simple:

- $y=ax+b$

C'est presque ça, il faut prendre en compte la notion d'erreurs et nous obtenons :

- $\hat{y} = \beta_0+\beta_1x_1+\beta_2x_2 ... +\beta_nx_n +\epsilon$


Avec $\epsilon=y_i -\hat{y}$

Explication des termes :
-	$y$ : La variable dépendante (ex: le prix d’une maison).
- $\hat{y}$ : Notre variable **<span style="color:red">prédite</span>**
-	$x_1$, $x_2$ : Les variables explicatives (ex: surface, nombre de chambres).
-	$\beta_0$ : L’ordonnée à l’origine (intercept), point où le plan coupe l’axe y.
-	$\beta_1$, $\beta_2$ : Les coefficients de régression représentant l’impact de chaque variable.
-	$\varepsilon$ : L’erreur résiduelle qui capte les variations inexpliquées.

---

### **Le but du jeu**

Notre algorithme a une seule mission : trouver l’intercept $\beta_0$ ainsi que les coefficients de régression $\beta_1, \dots, \beta_n$ qui minimisent l’erreur $\varepsilon$, définie comme la différence entre les valeurs observées et les valeurs prédites.
#### **Un petit éxemple**
![width:500](images/reggif.gif)
[Visualisation interactive de la régression par moindres carrés ordinaires](https://setosa.io/ev/ordinary-least-squares-regression/)

**&#129304; Intuition: pourquoi l'erreur est elle au carré  ?** (idée KPI)

---
### **Comment trouver cette solution ?**

Il éxiste deux méthodes que nous allons voir dans ce cours:
- La méthodes des moindres carrés 
- La descente de gradient

---
<!-- header: La méthode des moindres carrés -->

### **La méthode des moindres carrés**

1. Trouver $\hat{\beta}$ les coefficients estimés
2. Effectuer la prediction afin de determiner l'erreur $\epsilon$

Nous avons:
$\vec{Y}=X\vec{β}+\vec{u}$

Ceux qui nous donne pour une seule observation : 

$\vec{Y}=β_0+β_1X_1+β_2X_2+…+β_kX_k+\epsilon_1$

Et pour l'ensemble de nos observations nous obtenons : 
$\begin{bmatrix}
y_1 \\
y_2 \\
\vdots \\
y_n
\end{bmatrix}=
\begin{bmatrix}
1 & x_{11} & x_{12} & \dots & x_{1p} \\
1 & x_{21} & x_{22} & \dots & x_{2p} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_{n1} & x_{n2} & \dots & x_{np}
\end{bmatrix}
\begin{bmatrix}
\beta_0 \\
\beta_1 \\
\vdots \\
\beta_p
\end{bmatrix}
+
\begin{bmatrix}
\varepsilon_1 \\
\varepsilon_2 \\
\vdots \\
\varepsilon_n
\end{bmatrix}$

---

### **La méthode des moindres carrés**

La méthode des moindres carrés nous dit que pour obtenir les coefficients estimés $\hat{\beta}$, nous devons effectuer le calcul suivant:

- $\hat{\beta}= (X^TX)^{-1}X^Ty$

Prenons l'éxemple suivant : 


$\mathbf{X} =
\begin{bmatrix}
1 & 1 & 2 \\
1 & 2 & 4 \\
1 & 3 & 5 \\
\end{bmatrix}
\quad
\mathbf{y} =
\begin{bmatrix}
8 \\
12 \\
15 \\
\end{bmatrix}$

<br>

**Je fais quoi avec les deux matrices $X$ et $Y$ précedente ?** 

---

### **La méthode des moindres carrés**
1. Calcul de la transposée de $X$
$\mathbf{X}^T =
\begin{bmatrix}
1 & 1 & 1 \\
1 & 2 & 3 \\
2 & 4 & 5 \\
\end{bmatrix}$

2. Calcul du produit scalaire entre $X^T$ et $X$

- $X^T\cdot X=\begin{bmatrix}
1 & 1 & 1 \\
1 & 2 & 3 \\
2 & 4 & 5 \\
\end{bmatrix} \cdot \begin{bmatrix}
1 & 1 & 2 \\
1 & 2 & 4 \\
1 & 3 & 5 \\
\end{bmatrix}= \begin{bmatrix}
1 & 6 & 11 \\
6 & 14 & 25 \\
11 & 25 & 45 \\
\end{bmatrix}$

3. Calculons $X^T \cdot y$
- $X^T \cdot y= \begin{bmatrix}
1 & 1 & 1 \\
1 & 2 & 3 \\
2 & 4 & 5 \\
\end{bmatrix} \cdot \begin{bmatrix}
8 \\
12 \\
15 \\
\end{bmatrix}= \begin{bmatrix} 
35 \\
77 \\ 
139 \end{bmatrix}$
---

### **La méthode des moindres carrés**

4. Calculons $(X^TX)^{-1}$

- $(\mathbf{X}^T \mathbf{X})^{-1} =
\begin{bmatrix}
5 & 5 & -4 \\
5 & 14 & -9 \\
-4 & -9 & 6 \\
\end{bmatrix}$

5. Calculons maintenant nos coefficients $\beta$

- $\hat{\boldsymbol{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y} =
\begin{bmatrix}
4 \\
2 \\
1 \\
\end{bmatrix}$

Notre modèle de régression linéaire aura donc la formule suivante : 

- $\hat{y} = 4 + 2x_1 + 1x_2$

###### **Question: Comment je calcule les erreurs ?** 

---

<!-- header: ❌ Limites de la méthode des moindres carrés -->


## &#9940; Quand **ne pas utiliser** la méthode des moindres carrés (OLS) ?

---

### &#128200; 1. Multicolinéarité (variables corrélées)

- **Problème** : $\mathbf{X}^T \mathbf{X}$ non inversible
- **Effet** : Coefficients instables ou non calculables
- **Exemple** : $x_2 = 2x_1$ → Redondance
- **Solution** : Régression **Ridge (L2)** ou **Lasso (L1)**

---

### &#128202; 2. Trop de variables ($p \gg n$) ou $p=features$ et $n=observation$

- **Problème** : Trop de dimensions → sur-apprentissage
- **Effet** : Le modèle s’ajuste au bruit
- **Solution** :  **réduction de dimension** (PCA)

---

### &#128683; 3. Données avec des **outliers**

- **Problème** : OLS est très sensible aux grandes erreurs (tous les points sont utilisés)
- **Effet** : Une valeur extrême peut fausser la droite
- **Solution** : Régression Linéaire ( **Huber**)



---

### &#128273; 4. Relation **non linéaire**

- **Problème** : Le lien entre les variables n’est pas une droite
- **Effet** : Mauvaise qualité de prédiction
- **Solution** : 
  - Régression **polynomiale**
  - **Transformation des variables**
  - **Modèles non linéaires** (forêts aléatoires, réseaux de neurones…)

---

### &#128683; 5. Trop de données

- **Problème** : OLS est très sensible à toutes nos données 
- **Effet** : Elle s'adapte parfaitement 
- **Solution** : Régression Linéaire ( **Huber**)

---

###  Résumé des cas à éviter

| Situation                | Problème                          | Solution                   |
|--------------------------|-----------------------------------|----------------------------|
| Colinéarité              | $X^T X$ non inversible        | Ridge, Lasso               |
| Trop de variables        | Sur-apprentissage                 | Lasso, PCA                 |
| Valeurs aberrantes       | Instabilité                       | Huber              |
| Relation non linéaire    | Mauvais ajustement                | Régression non linéaire    |

 
---
<!-- header: La descente de gradient -->

### **La descente de gradient** - **Différence avec les moindres carrés (OLS)**

- **OLS** : méthode analytique → donne une **solution unique** (si possible)
- **Descente de gradient** : méthode **numérique**, dépend :
  - du **point de départ**
  - du **learning rate**
  - du **nombre d’itérations**
  
Elle peut conduire à **plusieurs minima locaux** (surtout dans des modèles non linéaires)

Le but du **SGD** est de trouver un minimum dans son paradigme !

---


### **La descente de gradient**

Une méthode **itérative** qui, à chaque étape, cherche à se rapprocher du **minimum** d’une **fonction de perte** ou loss function (*très important*).
C'est en se rapprochant du minimum de la fonction de perte que nous nous rapprocherons de nos $\beta$ optimaux.

Utilisé dans plusieurs algorithmes :
- Regression linéaire
- Régression logistique 
- Réseaus de neuronnes 

Son but est de minimiser l'erreurs $\epsilon$ en ajustant progressivement les poids $\beta_n$ associés aux différentes features $x_n$

---


### **Visuellement, voici un exemple de cet algorithme**
<div style="display: flex; justify-content: center; align-items: center;">

 <img width="400" height="300" src="images/reggif.gif" alt="Régression linéaire par moindres carrés" title="Ajustement de la droite de régression">
  <img width="400" height="350" src="images/gjDzm.gif" alt="Descente de gradient" title="Convergence vers le minimum de la fonction de coût">
</div>

**Des idées ?**

La notion d'erreur est très importante il faut reussir à la représenter mathématiquement, à la calculer ! 

---
<!-- header: La descente de gradient: La loss function -->

### **Deux notions importantes pour comprendre cet algorithme**

1. La loss function (représentative de l'érreur **globale** à chaque itération de notre algorithme)
2. Le learning rate 

---


### **La loss function**

Nous allons d'abord parler de la **loss function**



Une **fonction de perte (loss function)** mesure **l’erreur** entre la sortie prédite  $\hat{y}$ et la sortie réelle $y$.

Prenons le cas de la MSE (il en existe plusieurs on en parle un peu plus tard):

- $\mathcal{L}(\beta) = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2$

Elle nous donne un **score**:
- Plus ce score est elevé plus mes prédictions sont **....** ?
- Plus ce score est bas plus mes prédictions sont **....** ? 
- Pourquoi au carré ? 
---

### **Représentation visuelle de la loss function**


<div style="display: flex; justify-content: space-between; align-items: center;">
  <img width="400" height="400" src="images/mse.png">
  <ul>
    <li>Les points sont mes observations, mon dataset</li>
    <li>Les carrés rouges représentent ? </li> 
    <li>La droite est ma droite de régression</li>

 
  </ul>
</div>


---

### &#128201; Un éxemple concret

On dispose d’un jeu de données simple :

| x (surface en m²) | y (prix en k€) |
|-------------------|----------------|
| 1                 | 2              |
| 2                 | 4              |
| 3                 | 6              |

On cherche une **droite** de la forme :
$
\hat{y} = \beta_0 + \beta_1 x
$

Objectif : trouver $\beta_0, \beta_1$ qui **minimisent l’erreur** entre les $y_i$ et les $\hat{y}_i$

---

### &#128200; Fonction de perte (MSE)

On minimise la **somme des carrés des erreurs** :

$
\mathcal{L}(\beta_0, \beta_1) = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2 = \frac{1}{n} \sum_{i=1}^n (y_i - (\beta_0 + \beta_1 x_i))^2
$

Cette fonction est **convexe** → elle a **un unique minimum**.

On veut **trouver ce minimum** à l’aide de la **descente de gradient**.

---

### 📉 Slide 3 — Visualisation de la perte

La fonction $\mathcal{L}(\beta_1)$ peut être **visualisée** comme une courbe :

![width:500px](https://upload.wikimedia.org/wikipedia/commons/1/1b/Gradient_descent.svg)

- L’axe horizontal : valeurs possibles de $\beta_1$
- L’axe vertical : valeur de la perte
- Le **minimum** correspond à la **meilleure droite**

---

### 🧮 Slide 4 — Calcul de la tangente : la dérivée

On calcule la **dérivée** de la fonction de perte pour connaître la **pente locale** :

$
\frac{\partial \mathcal{L}}{\partial \beta_1} = -\frac{2}{n} \sum_{i=1}^n x_i (y_i - (\beta_0 + \beta_1 x_i))
$

💡 Cette dérivée **donne la direction de la tangente** :  
- Si $\frac{d\mathcal{L}}{d\beta_1} > 0$ → pente positive → il faut **descendre à gauche**
- Si $< 0$ → pente négative → **descendre à droite**

---

### 🔁 Slide 5 — Mise à jour des paramètres

À chaque itération, on met à jour les paramètres comme ceci :

$
\beta_1 \leftarrow \beta_1 - \eta \cdot \frac{\partial \mathcal{L}}{\partial \beta_1}
$

$
\beta_0 \leftarrow \beta_0 - \eta \cdot \frac{\partial \mathcal{L}}{\partial \beta_0}
$

- $\eta$ : learning rate (pas de mise à jour)
- On répète jusqu’à **convergence**

---

### 🧪 Slide 6 — Exemple chiffré simple

Soit 3 points : $(1, 2), (2, 4), (3, 6)$

On initialise $\beta_0 = 0, \beta_1 = 0$  
Learning rate $\eta = 0.1$

1. $\hat{y}_i = 0$, donc $y_i - \hat{y}_i = y_i$
2. Calcul du gradient :
   $
   \frac{\partial \mathcal{L}}{\partial \beta_1} = -\frac{2}{3} \left(1 \cdot 2 + 2 \cdot 4 + 3 \cdot 6\right) = -\frac{2}{3}(2 + 8 + 18) = -\frac{2}{3} \cdot 28 = -18.67
   $
3. Mise à jour :
   $
   \beta_1 \leftarrow 0 + 0.1 \cdot 18.67 = 1.867
   $

✅ On s'est rapproché du minimum !

---

### 🧠 Slide 7 — Conclusion

- La **tangente** indique la direction pour **réduire la perte**
- Le gradient est utilisé pour **ajuster les poids**
- À chaque itération, le modèle **apprend à mieux prédire**
- La descente de gradient est au cœur de **tous les modèles d’apprentissage supervisé**

---

# &#128202; Régression Linéaire

## &#128204; Objectifs

- Comprendre la **régression linéaire**
- Expliquer **l'ajustement des coefficients**
- Voir comment **trouver le minimum**
- Implémenter avec **Scikit-Learn**

---

# &#128269; Définition de la Régression Linéaire

La régression linéaire est un **modèle statistique** utilisé pour prédire une variable $y$ en fonction d’une ou plusieurs variables explicatives $x$.

### &#128197; Forme générale :

$$
y = \beta_0 + \beta_1 x + \varepsilon
$$

- **$y$** : Variable à prédire (dépendante)
- **$x$** : Variable explicative (indépendante)
- **$\beta_0, \beta_1$** : Coefficients du modèle
- **$\varepsilon$** : Erreur résiduelle

---

# &#128295; Principe de la Régression Linéaire

L’objectif est de **trouver la droite** qui minimise l’écart entre les points et la prédiction.

&#128161; **On cherche à minimiser la somme des erreurs au carré (MSE) :**

$$
J(\beta_0, \beta_1) = \sum (y_i - (\beta_0 + \beta_1 x_i))^2
$$

- **Plus $ J $ est petit, meilleur est l’ajustement.**

---

# &#128293; Trouver le Minimum

On utilise **deux méthodes principales** pour minimiser la fonction de coût :

1. **Moindres Carrés Ordinaires (OLS)** : 
   - Calcul exact basé sur les dérivées partielles.

2. **Descente de Gradient** :
   - Approche itérative qui ajuste progressivement $ \beta_0, \beta_1 $.

---

# &#128220; Méthode des Moindres Carrés

Pour minimiser $ J(\beta_0, \beta_1) $, on résout :

$$
\beta_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}
$$

$$
\beta_0 = \bar{y} - \beta_1 \bar{x}
$$

✅ **Avantage** : Solution exacte et rapide

🚨 **Inconvénient** : Ne fonctionne pas bien si $ X $ est trop grand

---

# &#9889; Descente de Gradient

La descente de gradient met à jour $ \beta_0 $ et $ \beta_1 $ en fonction du gradient de la fonction de coût :

$$
\beta_j = \beta_j - \alpha \frac{\partial J}{\partial \beta_j}
$$

avec **$ \alpha $** le **taux d’apprentissage**.

🚀 **Idée** : On ajuste progressivement les paramètres jusqu’à convergence.

---

# &#128187; Implémentation en Python

📌 **Exemple avec Scikit-Learn**

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Génération des données
X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
y = np.array([2, 3, 4, 5, 6])

# Création du modèle
model = LinearRegression()
model.fit(X, y)

# Prédictions
y_pred = model.predict(X)

# Affichage
plt.scatter(X, y, color='blue', label='Données')
plt.plot(X, y_pred, color='red', label='Régression')
plt.legend()
plt.show()
```

✅ **Facile à utiliser !**

---

# &#128221; Résumé

✔ **Régression linéaire** = Ajustement d’une droite aux données.
✔ **Méthodes d’optimisation** : Moindres carrés et Descente de gradient.
✔ **Scikit-Learn** simplifie l’implémentation.

💡 **Prochaine étape : Régression logistique !** 🚀