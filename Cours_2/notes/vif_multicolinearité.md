---
# 📊 Colinéarité et VIF (Variance Inflation Factor)

## 1. Pourquoi se préoccuper de la colinéarité ?

La colinéarité désigne une situation où **deux ou plusieurs variables explicatives** d'un modèle de régression sont **fortement corrélées** entre elles.

### ⚠️ Problèmes engendrés :
- Les **coefficients deviennent instables** et difficiles à interpréter.
- Les **valeurs p** peuvent être trompeuses (ex. une variable utile peut apparaître non significative).
- Le modèle peut **surréagir** à de petits changements dans les données.

---

## 2. Le VIF (Variance Inflation Factor)

Le **VIF** mesure combien la **variance estimée d'un coefficient** est **amplifiée à cause de la colinéarité** avec les autres variables du modèle.

### Formule :

$\text{VIF}_j = \frac{1}{1 - R_j^2}$

- $R_j^2$ : coefficient de détermination obtenu en régressant la variable $X_j$ sur toutes les autres variables explicatives.

### Interprétation des valeurs de VIF :

| VIF            | Interprétation                          |
|----------------|-------------------------------------------|
| $\approx 1$ | Aucune corrélation avec les autres       |
| $< 5$       | Corrélation modérée (acceptable)         |
| $> 5$       | Multicolinéarité potentielle            |
| $> 10$      | Multicolinéarité forte → à traiter      |

---

## 3. Solutions face à la colinéarité

- **Supprimer** l'une des variables fortement corrélées
- **Combiner** plusieurs variables (ex. via ACP)
- **Utiliser une régression régularisée** (Ridge, Lasso)
- **Repenser la modélisation** : a-t-on besoin de toutes les variables ?

---

## 4. Exemple en Python

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd

# Supposons que X soit un DataFrame avec les features
vif_data = pd.DataFrame()
vif_data["variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)
```

---

> 🚀 Le VIF est un outil clé pour **assurer la robustesse et la fiabilité** de vos régressions. Ne l'oubliez pas dans votre pipeline de modélisation !

