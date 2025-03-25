### Comprendre la notion de tangeante et de direction

Fonction de départ

$\mathcal{L}(\beta_0, \beta_1) = \frac{1}{n} \sum_{i=1}^n (y_i - (\beta_0 + \beta_1 x_i))^2$

On va dériver cette fonction par rapport à $\beta_1$.

---

️Étapes de dérivation

Étape 1 : développement du carré

$(y_i - (\beta_0 + \beta_1 x_i))^2
= \left( - (\beta_0 + \beta_1 x_i - y_i) \right)^2
= (\beta_0 + \beta_1 x_i - y_i)^2$

Donc on peut écrire :

$\mathcal{L}(\beta_1) = \frac{1}{n} \sum_{i=1}^n (\beta_0 + \beta_1 x_i - y_i)^2$

---

Étape 2 : dérivée d’une somme

$\frac{\partial \mathcal{L}}{\partial \beta_1} = \frac{1}{n} \sum_{i=1}^n \frac{\partial}{\partial \beta_1} \left[(\beta_0 + \beta_1 x_i - y_i)^2\right]$

On dérive chaque terme de la somme.

---

Étape 3 : dérivée de $u^2$ avec $u = \beta_0 + \beta_1 x_i - y_i$

$\frac{d}{d\beta_1} \left[ u^2 \right] = 2u \cdot \frac{du}{d\beta_1}$

Et ici :
$\frac{d}{d\beta_1} (\beta_0 + \beta_1 x_i - y_i) = x_i$

Donc :
$\frac{\partial \mathcal{L}}{\partial \beta_1} = \frac{1}{n} \sum_{i=1}^n 2(\beta_0 + \beta_1 x_i - y_i) \cdot x_i$

---

Forme finale simplifiée :

$\boxed{
\frac{\partial \mathcal{L}}{\partial \beta_1} = \frac{2}{n} \sum_{i=1}^n ( \hat{y}_i - y_i ) \cdot x_i
}$

Avec $\hat{y}_i = \beta_0 + \beta_1 x_i$

---

Intuition :
	•	Si $( \hat{y}_i - y_i )$ est grand, la pente est grande → le modèle est loin de la vérité
	•	Si les erreurs sont corrélées avec $x_i$, alors il faut ajuster $\beta_1$
	•	Le gradient est un signal qui dit : « dans quelle direction faut-il modifier $\beta_1$ pour réduire l’erreur »