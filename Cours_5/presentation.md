---
marp: true
theme: neobeam
paginate: true
size: 4:3
math: mathjax
html: true
header: Cours Esiroi 2026
footer: Data mining - Christopher de Boisvilliers
title: Cours 5 - Du texte aux vecteurs
style: |
  section pre {
    font-size: 19px;
    max-width: 100%;
    width: auto;
    background: #f4f7ff;
    border-left: 4px solid #3d65f6;
    border-radius: 8px;
    padding: 12px 16px;
    line-height: 1.45;
  }
  section pre code {
    font-size: 19px;
    color: #111827;
    background: none;
    padding: 0;
  }
---
<!-- _class: title -->

# Le Data Mining

<br/>

## Cours 5 — Du texte aux vecteurs

<br/>

Christopher de Boisvilliers

2026-11-02

---

<!-- header: ⭐️ Plan de la séance -->

### **Plan de la séance**

<div style="display:flex; gap:26px; margin-top:6px;">
<div style="flex:1.12; font-size:.92em;">

1. **Pourquoi le langage résiste**
2. **Du texte aux tokens**
3. **Distance d'édition**
4. **Sac de mots et cosinus**
5. **TF-IDF**
6. **Des mots aux vecteurs (Word2Vec)**
7. **Limites des méthodes vues**

</div>
<div style="flex:.88; border-left:2px solid #dbe4f7; padding-left:18px; font-size:.86em;">

**Les 5 séances**

<span style="color:#3d65f6; font-weight:700;">5 · NLP : du texte aux vecteurs</span>

6 · Embeddings et Transformers

7 · Recherche vectorielle

8 · RAG avec LangChain

9 · Évaluer et industrialiser

</div>
</div>

<div style="margin-top:10px; padding:10px 14px; background:#f4f7ff; border-radius:8px; font-size:.86em;">
Aujourd'hui : <strong>2 h 30 de cours</strong> — puis <strong>1 h de TP</strong>.<br/>
<span style="color:#4b5563;">Objectif : savoir transformer un texte en nombres, et savoir <em>pourquoi</em> chaque transformation change le résultat.</span>
</div>

---

### **Objectifs de la séance**

- **Préparer** un texte : normaliser, découper, filtrer
- **Comparer** deux textes : distance d'édition, cosinus
- **Construire** des vecteurs : comptages, TF-IDF
- **Comprendre** le principe de Word2Vec
- **Choisir** une représentation selon la question posée

> Aucune connaissance en linguistique n'est nécessaire : tout part d'exemples chiffrés.

---

<!-- header: ⭐️ Pourquoi le langage résiste -->

### **Deux phrases, une même scène**

<div style="display:flex; flex-direction:column; gap:12px; margin:14px 0 12px 0;">
<div style="background:#f4f7ff; border-left:5px solid #3d65f6; border-radius:8px; padding:12px 18px; font-size:1.1em;">
« <mark>Le</mark> chat dort <mark>sur</mark> <mark>le</mark> canapé. »
</div>
<div style="background:#f4f7ff; border-left:5px solid #3d65f6; border-radius:8px; padding:12px 18px; font-size:1.1em;">
« Un félin se repose <mark>sur</mark> <mark>le</mark> sofa. »
</div>
</div>

<div style="text-align:center; font-size:.78em; color:#4b5563; white-space:nowrap;">
13 occurrences · 10 formes · <strong>2 formes communes</strong> (<code>le</code>, <code>sur</code>) · <strong>0 mot de contenu commun</strong>
<div style="font-size:.86em; margin-top:2px; color:#4b5563;">« mot de contenu » = un mot qui porte du sens (nom, verbe, adjectif), par opposition aux mots outils.</div>
</div>

<div style="margin-top:14px; padding:12px 16px; border:1.5px dashed #3d65f6; border-radius:8px; font-size:.95em;">
Pour un humain, c'est la même scène.<br/>
Pour une méthode qui compte les mots, la similarité est faible et ne repose que sur <strong>deux mots outils</strong>.
</div>

<p style="text-align:center; margin-top:14px; font-size:.95em;">
C'est ce gouffre que ce cours comble, une brique à la fois.
</p>

---

### **Pourquoi est-ce si difficile ?**

- **Plusieurs sens** : `avocat` = un fruit ou un métier
- **Mots nouveaux** : `googliser`, `chanmé`
- **Écritures différentes** : `été`, `ÉTÉ`, `ete`
- **Synonymes** : `voiture` et `automobile` ne se ressemblent pas
- **Contexte** : le sens de `banque` dépend de la phrase

> Un même mot ne portant pas toujours le même sens, aucun comptage ne suffit.

---

### **Quatre niveaux d'analyse**

<p style="font-size:.85em; color:#4b5563; margin-bottom:6px;">
À ne pas confondre avec les quatre difficultés : ici on regarde <em>où</em> se situe le problème, sur <strong>quatre niveaux retenus dans ce cours</strong>.
</p>

![width:820px](./images/niveaux-analyse.svg)

<p style="font-size:.85em; color:#4b5563; margin-top:8px;">
Le NLP classique les traite séparément. La suite du parcours montrera des modèles qui les traitent ensemble.
</p>

---

### **La chaîne que nous allons construire**

![width:840px](./images/pipeline-cours5.svg)

<div style="margin-top:18px; display:flex; gap:12px; font-size:.85em;">
<div style="flex:1; border-left:4px solid #3d65f6; padding-left:12px;">
<strong>Aujourd'hui</strong><br/>
Texte → tokens → vecteurs
</div>
<div style="flex:1; border-left:4px solid #93a7f9; padding-left:12px;">
<strong>Séances 6 à 9</strong><br/>
Contexte → index → génération
</div>
</div>

<p style="margin-top:14px; font-size:.85em; color:#4b5563;">
Chaque brique sera construite à la main avant d'être appelée via une bibliothèque.
</p>

---

<!-- header: ⭐️ Du texte aux tokens -->

### **De la chaîne de caractères aux tokens**

<div style="display:flex; gap:22px; margin-top:4px;">
<div style="flex:1; font-size:.78em;">

**Le vocabulaire de base**

| Terme | Définition |
|---|---|
| **Type** | forme distincte |
| **Occurrence** | apparition d'un type dans le texte |
| **Token** | unité produite par le tokenizer (ici : un mot) |
| **Vocabulaire $V$** | ensemble des types |
| **Identifiant** | entier associé à un type |

</div>
<div style="flex:1; font-size:.84em;">

`le chat et le chien`

- **5 tokens** (occurrences)
- **4 types** (`le` apparaît 2 fois)
- $V$ = {`le`, `chat`, `et`, `chien`}
- identifiants : `le`→0, `chat`→1, `et`→2, `chien`→3

</div>
</div>

<div style="margin-top:12px; padding:10px 14px; background:#f4f7ff; border-radius:8px; font-size:.85em;">
Un modèle ne voit jamais de texte : il voit des <strong>identifiants</strong>. Toute la question est de savoir ce qu'on met <em>derrière</em> ces identifiants.<br/>
<span style="color:#4b5563;">Dans tout ce cours, <strong>token = un mot</strong>. En séance 6, le token deviendra un <strong>morceau de mot</strong> : c'est le même terme, mais pas la même unité.</span>
</div>

---

### **Un caractère n'est pas toujours un caractère**

```python
>>> len("é")                               # forme composée (NFC)
1
>>> len(unicodedata.normalize("NFD", "é")) # e + accent combinant
2
```

<div style="margin-top:10px; font-size:.9em;">

- `len()` compte des **points de code**, pas des caractères perçus (une lettre accentuée peut en occuper deux).
- Conséquence : deux textes visuellement identiques ne sont pas forcément égaux caractère par caractère.
- D'où, souvent, une **normalisation avant de comparer** — mais un tokenizer préentraîné peut imposer la sienne.

</div>

<div style="margin-top:12px; padding:10px 14px; border-left:4px solid #3d65f6; background:#f4f7ff; border-radius:6px; font-size:.85em;">
Règle pratique : <code>unicodedata.normalize("NFC", texte)</code> avant de comparer deux chaînes — sinon, suivre la normalisation du tokenizer utilisé.
</div>

---

### **Normaliser, c'est décider ce qu'on perd**

| Décision | Quand la prendre | Ce qu'on perd |
|---|---|---|
| minuscules | presque toujours | la casse (`Apple` ≠ `apple`) |
| supprimer les accents | recherche tolérante | `cote` / `côté` / `coté` |
| retirer la ponctuation | sac de mots | le point d'interrogation, l'emphase |
| retirer les chiffres | textes littéraires | `30 %`, `COVID-19` |
| espaces multiples | texte continu | l'indentation d'un code |

<div style="margin-top:14px; padding:10px 14px; background:#fff4e5; border-left:4px solid #d97706; border-radius:6px; font-size:.86em;">
Il n'existe pas de « bonne » normalisation : il existe des <strong>choix</strong>, et chacun se paie quelque part.
</div>

<p style="margin-top:10px; font-size:.85em; color:#4b5563;">
Un tokenizer préentraîné (BERT, GPT…) applique déjà sa propre normalisation : la refaire peut la contredire.<br/>
<strong>Règle simple :</strong> comparer deux chaînes → les normaliser <em>toutes les deux</em> dans la même forme (NFC par défaut, NFKC si ligatures ou compatibilité) ; passer du texte à un tokenizer préentraîné → ne rien normaliser soi-même.
</p>

---

### **Tokeniser : aucun découpage naïf ne suffit**

<div style="display:flex; gap:18px; font-size:.78em;">
<div style="flex:1;">

**Découper sur les espaces**

```
"l'ordinateur"  → ["l'ordinateur"]
"aujourd'hui"   → ["aujourd'hui"]
"porte-monnaie" → ["porte-monnaie"]
```

1 token chacune :<br/>
l'apostrophe et le trait d'union ne sont pas vus comme des frontières.

</div>
<div style="flex:1;">

**Découper avec `\w+`**

```
re.findall(r"\w+", "cœur été l'ordinateur")
→ ['cœur', 'été', 'l', 'ordinateur']
```

Les accents et `œ` passent.<br/>
Mais `l'ordinateur` est coupé en deux, et `\w` inclut chiffres et `_`.

</div>
</div>

<div style="margin-top:12px; padding:10px 14px; background:#f4f7ff; border-radius:8px; font-size:.86em;">
Aucune règle naïve n'est correcte pour toutes les tâches : le bon découpage dépend de l'<strong>unité</strong> qu'on veut manipuler.
</div>

---

### **Les stop words : un gain, un piège**

<div style="display:flex; gap:20px; margin-top:4px;">
<div style="flex:1; font-size:.85em;">

**Le gain**

- moins de dimensions donc des calculs plus rapides
- moins de bruit : les mots outils n'occupent plus l'essentiel des comptages

</div>
<div style="flex:1; font-size:.85em;">

**Le piège**

`je ne veux pas payer`

→ après retrait : `veux payer`

La négation a disparu. Le sens est inversé.

</div>
</div>

<div style="margin-top:14px; font-size:.88em;">

- Souvent retirés pour **BoW / TF-IDF** — mais c'est un **hyperparamètre** : sur des avis clients, `ne… pas` porte le signal.
- Un tokenizer de Transformer découpe avant tout filtrage : on ne supprime rien avant lui.

</div>

---

### **Stemming ou lemmatisation ?**

| Mot | Stemming (stem produit) | Lemmatisation |
|---|---|---|
| mangeons | `mang` | `manger` |
| mangera | `mang` | `manger` |
| mangé | `mang` | `manger` |
| mangeais | `mang` | `manger` |
| meilleur | `meilleur` | `bon` |

<div style="display:flex; gap:20px; margin-top:12px; font-size:.84em;">
<div style="flex:1;">

**Stemming** — règles de troncature (Snowball), sans dictionnaire.<br/>
Un stem n'est pas un radical linguistique : c'est la forme produite par l'algorithme.

</div>
<div style="flex:1;">

**Lemmatisation** — analyse morphologique et étiquette grammaticale.<br/>
Plus lente ; `meilleur → bon` dépend de l'analyseur.

</div>
</div>

---

### **Étiqueter la grammaire : le POS tagging**

<p style="font-size:.84em; color:#4b5563; margin:2px 0 6px 0;">
Chaque token reçoit une étiquette grammaticale (Universal POS). Exemple :
</p>

<div style="display:flex; gap:16px; font-size:.86em;">
<div style="flex:1.1;">

| token | étiquette |
|---|---|
| Le | `DET` |
| président | `NOUN` |
| parle | `VERB` |
| de | `ADP` |
| la | `DET` |
| banque | `NOUN` |

</div>
<div style="flex:1;">

**À quoi ça sert**

- **lever une ambiguïté** : `la fermeture` (nom) vs `fermer` (verbe)
- **lemmatiser juste** : `suis` → `être` ou `suivre` selon le contexte
- **préparer l'extraction d'entités** (séance 6)

</div>
</div>

<div style="margin-top:10px; padding:10px 14px; background:#f4f7ff; border-radius:8px; font-size:.84em;">
C'est un <strong>outil de pipeline</strong>, pas un concept de ce cours : on l'utilise, on ne l'implémente pas.
</div>

---

### **Ce qu'on garde pour la suite**

<div style="font-size:.88em;">

**1 · Les sous-mots (BPE, WordPiece)** — avec les sous-mots, « token » ne veut plus dire « mot » : c'est un morceau de mot, et ce sera le sens du terme en séance 6.

`incroyable` → `in` + `croy` + `able` (segmentation illustrative) : un mot inconnu devient une suite de morceaux connus.
C'est la réponse au problème des mots hors vocabulaire. Le principe est repris par tous les Transformers — BPE, WordPiece ou Unigram selon le modèle (séance 6).

**2 · Le POS tagging, en trois lignes**

Chaque token reçoit une étiquette (`DET`, `NOUN`, `VERB`… en Universal POS). Utile pour lever une ambiguïté et pour lemmatiser correctement. C'est un **outil de pipeline**, pas un concept de ce cours.

</div>

<div style="margin-top:16px; padding:12px 16px; border:1.5px dashed #3d65f6; border-radius:8px; font-size:.9em;">
On sait maintenant produire des tokens propres.<br/>
Question suivante : comment dire que <strong>deux textes se ressemblent</strong> ?
</div>

---

### **Le pipeline de prétraitement, de bout en bout**

![width:840px](./images/preprocessing-pipeline.svg)

<div style="display:flex; gap:16px; font-size:.8em; margin-top:2px;">
<div style="flex:1;">

**Les deux étapes optionnelles** (orange) ne le sont pas pour les mêmes raisons : les stop words allègent le vecteur, la lemmatisation rapproche les formes d'un même mot.

</div>
<div style="flex:1;">

**Le POS tagging** n'est pas une étape de filtrage : il fournit l'étiquette dont la lemmatisation a besoin (`suis` → `être` ou `suivre`).

</div>
</div>

<p style="font-size:.78em; color:#4b5563; margin-top:4px;">
Ordre à respecter : on ne filtre pas avant d'avoir tokenisé, et on ne lemmatise pas sans étiquette grammaticale.
</p>

---

### **Un exemple, étape par étape**

<p style="font-size:.86em; margin:2px 0 8px 0;">Phrase de départ : <code>Les chats d'Emily dorment sur le canapé du salon.</code></p>

<table style="border-collapse:collapse; width:100%; font-size:.8em;">
<tr>
<th style="width:26%; text-align:left; padding:7px 10px; background:#3d65f6; color:#fff; white-space:nowrap;">Étape</th>
<th style="text-align:left; padding:7px 10px; background:#3d65f6; color:#fff;">Résultat</th>
</tr>
<tr><td style="padding:7px 10px; border-bottom:1px solid #e5e7eb; white-space:nowrap;"><strong>1. Normaliser</strong></td><td style="padding:7px 10px; border-bottom:1px solid #e5e7eb;"><code>les chats d'emily dorment sur le canape du salon</code></td></tr>
<tr><td style="padding:7px 10px; border-bottom:1px solid #e5e7eb; white-space:nowrap;"><strong>2. Tokeniser</strong></td><td style="padding:7px 10px; border-bottom:1px solid #e5e7eb;"><code>["les", "chats", "emily", "dorment",<br/>&nbsp;&nbsp;"sur", "le", "canape", "du", "salon"]</code></td></tr>
<tr><td style="padding:7px 10px; border-bottom:1px solid #e5e7eb;"><strong>3. Filtrer</strong></td><td style="padding:7px 10px; border-bottom:1px solid #e5e7eb;">rien à retirer ici (pas de ponctuation, pas de chiffre)</td></tr>
<tr><td style="padding:7px 10px; border-bottom:1px solid #e5e7eb; white-space:nowrap;"><strong>4. Stop words</strong></td><td style="padding:7px 10px; border-bottom:1px solid #e5e7eb;"><code>["chats","emily","dorment","canape","salon"]</code></td></tr>
<tr><td style="padding:7px 10px; border-bottom:1px solid #e5e7eb; white-space:nowrap;"><strong>5. Étiqueter (POS)</strong></td><td style="padding:7px 10px; border-bottom:1px solid #e5e7eb;"><code>chats/NOUN · dorment/VERB · canape/NOUN · salon/NOUN</code></td></tr>
<tr><td style="padding:7px 10px;"><strong>6. Lemmatiser</strong></td><td style="padding:7px 10px;"><code>["chat","emily","dormir","canape","salon"]</code></td></tr>
</table>

<p style="font-size:.78em; color:#4b5563; margin-top:8px;">C'est la liste finale qui entre dans le dataset — pas la phrase d'origine.</p>

---

### **Ce qu'on garde dans le dataset**

<table style="border-collapse:collapse; width:100%; font-size:.76em;">
<tr>
<th style="text-align:left; padding:6px 8px; background:#3d65f6; color:#fff;">id</th>
<th style="text-align:left; padding:6px 8px; background:#3d65f6; color:#fff;">texte brut</th>
<th style="text-align:left; padding:6px 8px; background:#3d65f6; color:#fff;">tokens</th>
<th style="text-align:center; padding:6px 8px; background:#3d65f6; color:#fff;">n</th>
</tr>
<tr><td style="padding:6px 8px; border-bottom:1px solid #e5e7eb;">1</td><td style="padding:6px 8px; border-bottom:1px solid #e5e7eb;">Les chats d'Emily dorment sur le canapé.</td><td style="padding:6px 8px; border-bottom:1px solid #e5e7eb;"><code>chat emily dormir canape</code></td><td style="text-align:center; padding:6px 8px; border-bottom:1px solid #e5e7eb;">4</td></tr>
<tr><td style="padding:6px 8px; border-bottom:1px solid #e5e7eb;">2</td><td style="padding:6px 8px; border-bottom:1px solid #e5e7eb;">Le chien aboie dans le jardin.</td><td style="padding:6px 8px; border-bottom:1px solid #e5e7eb;"><code>chien aboyer jardin</code></td><td style="text-align:center; padding:6px 8px; border-bottom:1px solid #e5e7eb;">3</td></tr>
<tr><td style="padding:6px 8px;">3</td><td style="padding:6px 8px;">Un félin se repose sur le sofa.</td><td style="padding:6px 8px;"><code>felin reposer sofa</code></td><td style="text-align:center; padding:6px 8px;">3</td></tr>
</table>

- **Toujours garder** la colonne `texte brut` : sans elle, impossible de revenir en arrière si le nettoyage a détruit une information
- **Une ligne = un document** (une phrase, un paragraphe, un avis…)
- **Colonnes en plus** selon la tâche : étiquettes, POS, longueur, date

> Le nettoyage se choisit selon la tâche. Pour de la classification d'avis, on garde `ne… pas`. Pour de la recherche par mots-clés, on retire les stop words.

---

<!-- header: ⭐️ Distance d'édition -->

### **Deux chaînes se ressemblent-elles ?**

<div style="display:flex; flex-direction:column; gap:10px; margin-top:6px; font-size:.86em;">
<div style="background:#f4f7ff; border-radius:8px; padding:12px 16px;">
<strong>Une faute de frappe</strong> — <code>ordinateur</code> / <code>ordinatuer</code><br/>
L'utilisateur a tapé trop vite.
</div>
<div style="background:#f4f7ff; border-radius:8px; padding:12px 16px;">
<strong>Une flexion</strong> — <code>carton</code> / <code>cartons</code><br/>
Le même objet, deux formes.
</div>
<div style="background:#f4f7ff; border-radius:8px; padding:12px 16px;">
<strong>Un synonyme</strong> — <code>voiture</code> / <code>automobile</code><br/>
Le même objet, et pourtant une distance de <strong>8</strong>.
</div>
</div>

<p style="margin-top:12px; font-size:.9em;">
Peut-on mesurer la ressemblance <em>sans</em> passer par des vecteurs ? Commençons par le plus simple : les caractères.
</p>

---

### **Trois opérations, un coût de 1**

<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-top:10px; font-size:.8em; text-align:center;">
<div style="background:#f4f7ff; border-radius:10px; padding:14px 10px;">
<strong>Insertion</strong><br/><br/>
<code>chat</code> → <code>chats</code><br/><br/>
<span style="color:#4b5563;">ajouter <code>s</code></span>
</div>
<div style="background:#f4f7ff; border-radius:10px; padding:14px 10px;">
<strong>Suppression</strong><br/><br/>
<code>chats</code> → <code>chat</code><br/><br/>
<span style="color:#4b5563;">ôter <code>s</code></span>
</div>
<div style="background:#f4f7ff; border-radius:10px; padding:14px 10px;">
<strong>Substitution</strong><br/><br/>
<code>chat</code> → <code>chot</code><br/><br/>
<span style="color:#4b5563;">remplacer <code>a</code> par <code>o</code></span>
</div>
</div>

<div style="margin-top:16px; padding:12px 16px; border-left:4px solid #3d65f6; background:#f4f7ff; border-radius:6px; font-size:.9em;">
<strong>Distance de Levenshtein</strong> = coût minimal de la suite d'opérations qui transforme une chaîne en l'autre.
</div>

---

### **La récurrence**

<div style="font-size:.78em;">

$$\text{lev}(i,j)=\min\begin{cases}\text{lev}(i-1,j)+1 & \text{supprimer } a_i\\[2pt] \text{lev}(i,j-1)+1 & \text{ajouter } b_j\\[2pt] \text{lev}(i-1,j-1)+[a_i\neq b_j] & \text{substituer, ou conserver si } a_i=b_j\end{cases}$$

$$\text{conditions initiales :}\quad \text{lev}(i,0)=i \qquad \text{lev}(0,j)=j$$

</div>

<div style="font-size:.86em; margin-top:4px;">

- $\text{lev}(i,j)$ = distance entre les **$i$ premiers caractères** de $a$ et les **$j$ premiers** de $b$.
- $[a_i \neq b_j]$ vaut **0 si les caractères sont égaux, 1 sinon**.
- On lit le résultat dans la **dernière case** de la matrice.
- Les conditions initiales ne sont pas décoratives : sans elles, la récurrence ne démarre pas.

</div>

---

### **La matrice : initialisation**

<p style="font-size:.82em; color:#4b5563; margin:2px 0 0 0;">
<em>a</em> = <code>chat</code> (lignes) · <em>b</em> = <code>chats</code> (colonnes) · la première ligne et la première colonne sont les conditions initiales.
</p>
<table style="border-collapse:collapse;margin:10px auto;">
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'></th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>ε</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>c</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>h</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>a</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>t</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>s</th></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>ε</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>0</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>3</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>4</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>5</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>c</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>h</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>a</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>t</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td></tr>
</table>
<p style="font-size:.82em; text-align:center; color:#4b5563; margin-top:2px;">
Transformer 0 caractère en <em>j</em> caractères coûte <em>j</em> insertions — et inversement.
</p>

---

### **La matrice : on remplit case par case**

<p style="font-size:.82em; color:#4b5563; margin:2px 0 0 0;">
Chaque case regarde ses <strong>trois voisines</strong> (haut, gauche, diagonale) et prend le minimum. Ici le calcul de la case ligne <code>a</code>, colonne <code>a</code>.
</p>
<table style="border-collapse:collapse;margin:10px auto;">
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'></th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>ε</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>c</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>h</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>a</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>t</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>s</th></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>ε</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>0</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>3</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>4</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>5</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>c</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>0</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>3</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>4</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>h</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>0</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>3</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>a</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>3</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#fff4e5;border:2px solid #d97706;font-weight:700;'>0</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>t</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;color:#c7cedb;background:#fafbfe;'>·</td></tr>
</table>
<div style="font-size:.82em; margin-top:2px;">
haut = 1+1 = 2 · gauche = 1+1 = 2 · diagonale = 0+0 = <strong>0</strong> (mêmes caractères) → <strong>0</strong>
</div>

---

### **La matrice : le résultat**

<p style="font-size:.82em; color:#4b5563; margin:2px 0 0 0;">
La dernière case donne la distance : <strong>1</strong>. Le chemin surligné montre l'opération retenue.
</p>
<table style="border-collapse:collapse;margin:10px auto;">
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'></th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>ε</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>c</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>h</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>a</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>t</th><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>s</th></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>ε</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#c7d4f7;font-weight:700;'>0</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>3</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>4</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>5</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>c</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#c7d4f7;font-weight:700;'>0</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>3</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>4</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>h</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#c7d4f7;font-weight:700;'>0</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>3</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>a</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>3</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#c7d4f7;font-weight:700;'>0</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td></tr>
<tr><th style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#eef2ff;font-weight:700;color:#111827;'>t</th><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>4</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>3</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>2</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;'>1</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#c7d4f7;font-weight:700;'>0</td><td style='width:56px;height:40px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:19px;background:#c7d4f7;font-weight:700;'>1</td></tr>
</table>
<div style="margin-top:6px; padding:10px 14px; background:#f4f7ff; border-left:4px solid #3d65f6; border-radius:6px; font-size:.86em;">
<code>chat</code> → <code>chats</code> : on conserve <code>c</code>, <code>h</code>, <code>a</code>, <code>t</code>, puis on <strong>insère</strong> <code>s</code>. Coût total : <strong>1</strong>.
</div>

---

### **Normaliser la distance, et les autres cas**

<div style="font-size:.9em; text-align:center;">
<p style="margin:0 0 2px 0;">Similarité normalisée :</p>

$$
1-\frac{\mathrm{lev}(a,b)}{\max(|a|,|b|)}
$$

</div>

| Paire | Distance | Similarité |
|---|---|---|
| `chats` / `chat` | 1 | 0,80 |
| `carton` / `cartons` | 1 | 0,86 |
| `chien` / `chats` | 3 | 0,40 |
| `ordinateur` / `ordinatuer` | 2 | 0,80 |
| `voiture` / `automobile` | 8 | 0,20 |

<div style="margin-top:10px; font-size:.82em; color:#4b5563;">
La formule de normalisation ci-dessus est une <strong>convention</strong> parmi d'autres (on divise aussi parfois par la somme des longueurs).
En <strong>Damerau-Levenshtein</strong>, une transposition compte pour 1 : <code>ordinatuer</code> revient alors à une distance de 1.<br/>
Par convention, la similarité de deux chaînes vides vaut 1.
</div>

---

### **Où ça marche, où ça casse**

<div style="display:flex; gap:20px; margin-top:4px;">
<div style="flex:1; font-size:.84em;">

**Ça marche**

- correction orthographique
- dédoublonnage de fichiers ou de contacts
- recherche approximative (fuzzy)
- alignement de séquences (avec des coûts adaptés)

</div>
<div style="flex:1; font-size:.84em;">

**Ça casse**

- `voiture` / `automobile` : distance 8 sur 10, sens identique
- aucune notion de mot ni de sens
- coût $O(nm)$ sur de longs textes
- comparer des documents est possible, mais coûteux et rarement pertinent

</div>
</div>

<div style="margin-top:14px; padding:12px 16px; border:1.5px dashed #3d65f6; border-radius:8px; font-size:.9em;">
On a mesuré des <strong>caractères</strong>. Pour comparer des <strong>textes</strong>, il faut changer d'unité : les mots.
</div>

---

<!-- header: ⭐️ Sac de mots et cosinus -->

### **L'idée du sac de mots**

<div style="font-size:.9em;">

Un document devient un **sac** : on garde *quels* mots et *combien* de fois, on jette l'ordre.

</div>

<div style="margin:10px 0; padding:12px 16px; background:#f4f7ff; border-left:4px solid #3d65f6; border-radius:6px; font-size:.9em;">
« le chat dort sur le canapé du salon »
→ <code>chat</code>×1 · <code>dort</code>×1 · <code>canapé</code>×1 · <code>salon</code>×1 · <code>le</code>×2 · <code>sur</code>×1 · <code>du</code>×1
</div>

<div style="display:flex; gap:20px; font-size:.86em;">
<div style="flex:1;">

**Le vocabulaire**

Sur nos 4 documents : **18 termes** — autant de types distincts.
C'est l'ensemble des colonnes de la matrice.

</div>
<div style="flex:1;">

**La question**

Deux sacs étant donnés, comment dire qu'ils se ressemblent — avec un **nombre**, pas une intuition ?

</div>
</div>

---

### **Le sac, mécaniquement**

![width:700px](./images/bow-mecanique.svg)

<div style="display:flex; gap:14px; align-items:center; margin-top:6px;">
<div style="flex:0 0 auto;">

![width:96px](./images/bow-sac.jpg)

</div>
<div style="flex:1; font-size:.84em; color:#4b5563;">
Deux phrases qui disent la même chose dans un autre ordre donnent <strong>le même vecteur</strong> : on perd l'ordre, on gagne un comptage comparable.
<br/><span style="font-size:.94em;">Le vecteur a <strong>une case par terme du vocabulaire</strong> : ici 5 termes, sur les 18 du corpus — les autres cases valent 0. La dimension est fixe, même si la phrase est courte.</span>
<br/><span style="font-size:.78em; color:#9aa4b8;">Le sac, au sens littéral : on y jette des morceaux, on perd leur disposition. Photo : Meritxell.canela, Wikimedia Commons, domaine public.</span>
</div>
</div>

---

### **Remplir les cases : présence ou comptage ?**

<p style="font-size:.84em; color:#4b5563; margin:2px 0 6px 0;">
Une seule phrase : <code>le chat dort, le chat dort encore</code> — vocabulaire de 4 termes.
</p>

<div style="display:flex; gap:20px; font-size:.86em;">
<div style="flex:1;">

**Présence (0 / 1)**

<table style="border-collapse:collapse;margin:6px auto;"><tr><th style='width:56px;height:30px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:15px;background:#3d65f6;color:#ffffff;font-weight:700;'>le</th><th style='width:56px;height:30px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:15px;background:#3d65f6;color:#ffffff;font-weight:700;'>chat</th><th style='width:56px;height:30px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:15px;background:#3d65f6;color:#ffffff;font-weight:700;'>dort</th><th style='width:56px;height:30px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:15px;background:#3d65f6;color:#ffffff;font-weight:700;'>encore</th></tr><tr><td style='width:56px;height:34px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:17px;'>1</td><td style='width:56px;height:34px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:17px;'>1</td><td style='width:56px;height:34px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:17px;'>1</td><td style='width:56px;height:34px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:17px;'>1</td></tr></table>

Le modèle sait que les mots sont là — pas combien de fois.

</div>
<div style="flex:1;">

**Comptage**

<table style="border-collapse:collapse;margin:6px auto;"><tr><th style='width:56px;height:30px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:15px;background:#3d65f6;color:#ffffff;font-weight:700;'>le</th><th style='width:56px;height:30px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:15px;background:#3d65f6;color:#ffffff;font-weight:700;'>chat</th><th style='width:56px;height:30px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:15px;background:#3d65f6;color:#ffffff;font-weight:700;'>dort</th><th style='width:56px;height:30px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:15px;background:#3d65f6;color:#ffffff;font-weight:700;'>encore</th></tr><tr><td style='width:56px;height:34px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:17px;'>2</td><td style='width:56px;height:34px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:17px;'>2</td><td style='width:56px;height:34px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:17px;'>2</td><td style='width:56px;height:34px;text-align:center;border:1px solid #dbe4f7;padding:0;font-family:Roboto Mono,monospace;font-size:17px;'>1</td></tr></table>

La répétition est conservée : c'est cette version que TF-IDF utilisera.

</div>
</div>

<div style="margin-top:10px; padding:10px 14px; background:#f4f7ff; border-radius:8px; font-size:.84em;">
Même phrase, même vocabulaire, <strong>deux vecteurs différents</strong> : le choix du score fait partie du modèle, pas du texte.
</div>

<p style="font-size:.66em; color:#9aa4b8; margin-top:4px;">D'après J. Brownlee, <em>A Gentle Introduction to the Bag-of-Words Model</em>, Machine Learning Mastery, 2019.</p>

---

### **La matrice documents × termes**

<p style="font-size:.82em; color:#4b5563; margin:2px 0 0 0;">
Lignes = documents · colonnes = termes du vocabulaire · valeur = nombre d'occurrences. 10 colonnes montrées sur 18.
</p>
<table style="border-collapse:collapse;margin:8px auto;">
<tr><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>document</th><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>chat</th><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>chien</th><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>dort</th><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>canapé</th><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>tapis</th><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>félin</th><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>sofa</th><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>salon</th><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>le</th><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>est</th><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>…</th></tr>
<tr><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>D1</th><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#dbe4f7;'>1</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#dbe4f7;'>1</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#dbe4f7;'>1</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#dbe4f7;'>1</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#b9c9f2;'>2</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;color:#9aa4b8;'>…</td></tr>
<tr><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>D2</th><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#dbe4f7;'>1</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#dbe4f7;'>1</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#dbe4f7;'>1</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#dbe4f7;'>1</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#b9c9f2;'>2</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;color:#9aa4b8;'>…</td></tr>
<tr><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>D3</th><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#dbe4f7;'>1</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#dbe4f7;'>1</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;color:#9aa4b8;'>…</td></tr>
<tr><th style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#eef2ff;font-weight:700;color:#111827;'>D4</th><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;'>0</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#b9c9f2;'>2</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#b9c9f2;'>2</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#b9c9f2;'>2</td><td style='width:58px;height:38px;text-align:center;border:1px solid #dbe4f7;padding:0;font-size:16px;font-family:Roboto Mono,monospace;background:#fafbfe;color:#9aa4b8;'>…</td></tr>
</table>
<p style="font-size:.82em; color:#4b5563; margin-top:2px;">
Chaque ligne est un <strong>vecteur de 18 nombres</strong>. La plupart valent zéro.
</p>

---

### **Un vecteur très creux**

<div style="display:flex; gap:22px; font-size:.86em; margin-top:6px;">
<div style="flex:1;">

**Ici**

- 18 dimensions
- **6 ou 7** valeurs non nulles par document
- densité moyenne **36 %** (26 cases sur 72) — parce que le corpus est minuscule

</div>
<div style="flex:1;">

**En réel**

- $10^4$ à $10^6$ dimensions
- quelques dizaines de mots par document
- densité **< 1 %**

</div>
</div>

<div style="margin-top:14px; padding:12px 16px; background:#fff4e5; border-left:4px solid #d97706; border-radius:6px; font-size:.88em;">
Sur un vrai corpus, un vecteur de 50 000 dimensions contient souvent moins de 100 valeurs non nulles.
C'est ce qu'on appelle un vecteur <strong>creux</strong> (<em>sparse</em>).
</div>

---

### **`fit` puis `transform` : la règle d'or**

```python
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)   # apprend le vocabulaire ET transforme
x = vectorizer.transform([requete])    # projette DANS ce vocabulaire
```

<div style="font-size:.86em; margin-top:8px;">

- `fit` **fige** la liste des colonnes — jusqu'au prochain `fit`, qui crée un autre modèle.
- `transform` ignore silencieusement les mots absents du vocabulaire.
- Conséquence : une requête peut très bien ne produire **aucun** signal.

</div>

<div style="margin-top:12px; padding:10px 14px; border-left:4px solid #3d65f6; background:#f4f7ff; border-radius:6px; font-size:.86em;">
Le vocabulaire fait partie du <strong>modèle</strong>. Recharger un modèle sans son vocabulaire, c'est comparer deux espaces différents.
</div>

---

### **Similarité cosinus**

<div style="display:flex; gap:18px; align-items:center;">
<div style="flex:1.1;">

![width:400px](./images/cosinus.svg)

</div>
<div style="flex:1; font-size:.92em;">

$$
\cos(\theta)=\frac{\mathbf a\cdot\mathbf b}{\|\mathbf a\|\,\|\mathbf b\|}
$$

- $\cos=1$ : même direction
- $\cos=0$ : vecteurs orthogonaux — aucun mot partagé
- ici jamais négatif : les comptages sont **non négatifs**

</div>
</div>

<div style="margin-top:10px; padding:10px 14px; background:#f4f7ff; border-radius:8px; font-size:.84em;">
Pourquoi pas la distance euclidienne ? Elle est sensible à la <strong>norme</strong> : $q$ et $2q$ désignent la même direction, mais sont à distance non nulle. Le cosinus ne regarde que l'<strong>angle</strong>.<br/><br/>La norme utilisée est la norme L2 : $\|\mathbf a\|=\sqrt{\sum_i a_i^2}$.<br/>Si l'un des deux vecteurs est nul, le cosinus est <strong>indéfini</strong> (0/0).
</div>

---

### **Exemple : requête « le chat »**

| Document | Contenu | Cosinus |
|---|---|---|
| D1 | le chat dort sur le canapé du salon | **0,671** |
| D2 | le chien dort sur le tapis du salon | 0,447 |
| D3 | un félin se repose sur un sofa | 0,000 |
| D4 | le salon est grand et le salon est clair | 0,365 |

<div style="font-size:.84em; margin-top:6px;">

- D1 gagne : $q\cdot D1 = 1\times2 + 1\times1 = 3$, $\|q\|=\sqrt{2}$, $\|D1\|=\sqrt{10}$ → $3/\sqrt{20}=0{,}671$.
- D2 et D4 ont le **même produit scalaire** ($q\cdot D = 2$) : c'est la norme qui tranche, $\sqrt{10}$ contre $\sqrt{15}$ → 0,447 contre 0,365.
- D3 tombe à **0** : aucun mot commun. Premier signal d'alarme.

</div>

---

### **Le sac perd l'ordre — et le sens**

<div style="display:flex; gap:18px; font-size:.84em; margin-top:4px;">
<div style="flex:1; background:#f4f7ff; border-radius:8px; padding:12px 14px;">

`le chien mord l'homme`<br/>
`l'homme mord le chien`

</div>
<div style="flex:1;">

Mêmes comptages, <strong>cosinus = 1</strong>.<br/>
Deux scènes opposées, un score parfait.

</div>
</div>

<div style="font-size:.86em; margin-top:12px;">

**La parade classique : les bigrammes**

`le chien`, `chien mord`, `mord l'homme`… On réintroduit un **ordre local entre mots adjacents**, au prix d'un espace de bigrammes théoriquement $V\times V$.

</div>

<div style="margin-top:10px; padding:10px 14px; background:#fff4e5; border-left:4px solid #d97706; border-radius:6px; font-size:.86em;">
Les bigrammes ajoutent de l'ordre local. Ils ne règlent <strong>ni</strong> les synonymes (<code>voiture</code> / <code>automobile</code> : cosinus 0) <strong>ni</strong> les mots inconnus.
</div>

---

### **Et si aucun mot n'est connu ?**

<div style="display:flex; gap:20px; font-size:.86em;">
<div style="flex:1;">

**Requête**<br/>
`animal de compagnie`

</div>
<div style="flex:1;">

**Vocabulaire du corpus**<br/>
`chat`, `chien`, `dort`, `canapé`, `tapis`, `félin`, `sofa`, `salon`…

</div>
</div>

<div style="margin-top:14px; padding:12px 16px; background:#fef2f2; border-left:4px solid #dc2626; border-radius:6px; font-size:.9em;">
Aucun terme commun → <strong>vecteur nul</strong> → cosinus <strong>indéfini</strong> (0/0), que scikit-learn affiche à 0 par convention.
</div>

<div style="font-size:.86em; margin-top:12px;">

Ce n'est pas un bug : un mot absent du vocabulaire n'a aucune colonne où s'écrire.
C'est pourtant le cas le plus fréquent en production : vocabulaire métier, fautes, abréviations, autre langue.

</div>

---

### **Le comptage brut a un défaut**

<div style="font-size:.88em;">

| Mot | Occurrences | Documents concernés |
|---|---|---|
| `le` | 6 | 3 sur 4 |
| `salon` | 4 | 3 sur 4 |
| `félin` | 1 | 1 sur 4 |

</div>

<div style="margin-top:10px; font-size:.88em;">

`le` est présent dans 3 documents sur 4 : il ne peut, au mieux, que distinguer D3 des trois autres.
`félin` n'apparaît que dans **un seul** document : il isole exactement la bonne réponse.

</div>

<div style="margin-top:14px; padding:12px 16px; border:1.5px dashed #3d65f6; border-radius:8px; font-size:.9em;">
Il faut donc <strong>donner un poids</strong> aux termes — et la bonne mesure de « rare » n'est pas la fréquence dans le document, mais le <strong>nombre de documents qui contiennent le mot</strong>. C'est tout l'objet de TF-IDF.
</div>

---

### **Le sac de mots : résumé**

- **Vecteur** : une case par mot du vocabulaire
- **Valeur** : présence (0/1) ou nombre d'occurrences
- **Cosinus** : compare la direction de deux vecteurs
- **Limites** : ordre perdu, synonymes séparés, mots inconnus ignorés

> Une requête sans aucun mot connu donne un vecteur nul — et un cosinus qui ne veut rien dire.

---

<!-- header: ⭐️ TF-IDF -->

### **L'idée : donner plus de poids à ce qui distingue**

<div style="display:flex; gap:20px; font-size:.86em; margin-top:4px;">
<div style="flex:1;">

**Le problème**

`le` est partout, donc il ne sépare rien.
`félin` est rare, donc il identifie.

Or le comptage brut les traite de la même façon : **1 occurrence = 1**.

</div>
<div style="flex:1;">

**L'idée**

Un terme est important s'il est :

- **fréquent dans le document** → TF
- **rare dans le corpus** → IDF

</div>
</div>

<div style="margin-top:10px; padding:10px 14px; background:#f4f7ff; border-left:4px solid #3d65f6; border-radius:6px; font-size:.84em;">
Intuition : un mot qui apparaît dans <em>tous</em> les documents ne peut pas servir à en choisir un.
</div>

![width:520px](./images/idf-rarete.svg)

<p style="font-size:.68em; color:#9aa4b8; margin-top:8px;">Salton &amp; Buckley (1988), <em>Term-weighting approaches in automatic text retrieval</em>.</p>

---

### **Les deux facteurs**

<div style="font-size:.86em;">

**TF** — nombre d'occurrences du terme dans le document (comptage brut dans scikit-learn) :

</div>

$$
\text{tf}(t,d)=n_{t,d}
$$

<div style="font-size:.86em; margin-top:6px;">

**IDF** — à quel point le terme est rare dans le corpus (convention scikit-learn, lissée) :

</div>

$$
\text{idf}(t)=\ln\!\left(\frac{1+N}{1+\text{df}(t)}\right)+1
\qquad
w_{t,d}=\text{tf}(t,d)\times\text{idf}(t)
$$

<div style="font-size:.82em; color:#4b5563; margin-top:6px;">
<em>N</em> = nombre de documents · <em>df(t)</em> = nombre de documents contenant <em>t</em> · les <em>+1</em> lissent le rapport : l'IDF ne peut jamais être nul ni négatif.<br/>
Le vecteur obtenu est ensuite <strong>normalisé en L2</strong>. La variante « classique » divise <em>tf</em> par la longueur du document — un facteur <strong>par document</strong>. Après normalisation L2, les deux conventions donnent des cosinus <strong>identiques</strong>.
</div>

---

### **Calcul sur notre corpus**

<p style="font-size:.82em; color:#4b5563; margin:0;">
N = 4 documents. Valeurs calculées avec la formule lissée ci-dessus.
</p>

| Terme | df | IDF |
|---|---|---|
| `le` | 3 | ln(5/4) + 1 = **1,223** |
| `salon` | 3 | ln(5/4) + 1 = **1,223** |
| `dort` | 2 | ln(5/3) + 1 = **1,511** |
| `chat` | 1 | ln(5/2) + 1 = **1,916** |
| `félin` | 1 | ln(5/2) + 1 = **1,916** |

<div style="margin-top:8px; font-size:.82em; color:#4b5563;">
Aucun terme n'est jamais annulé : <code>le</code>, présent dans 3 documents sur 4, garde un IDF de 1,22, soit <strong>1,57 fois moins</strong> qu'un mot unique — mais jamais zéro.
</div>

---

### **Requête « le chat », cette fois en TF-IDF**

| Document | Cosinus (comptages) | Cosinus (TF-IDF) |
|---|---|---|
| D1 | **0,671** | **0,641** |
| D2 | 0,447 | 0,288 |
| D3 | 0,000 | 0,000 |
| D4 | 0,365 | 0,214 |

<div style="font-size:.84em; margin-top:8px;">

- L'**ordre ne change pas** : D1 reste premier, et c'est normal — D1 contient vraiment `chat`.
- Ce qui change, c'est l'**écart** : D2 passe de 0,447 à 0,288, D4 de 0,365 à 0,214.
- TF-IDF ne réécrit pas la vérité : il **accentue les différences**.

</div>

---

### **Le cas où le classement bascule**

<p style="font-size:.84em; color:#4b5563; margin:0 0 4px 0;">
Requête : <code>félin salon</code>
</p>

| Document | Cosinus (comptages) | Cosinus (TF-IDF) |
|---|---|---|
| D1 le chat dort sur le canapé du salon | 0,224 | 0,144 |
| D2 le chien dort sur le tapis du salon | 0,224 | 0,144 |
| D3 un félin se repose sur un sofa | 0,236 | **0,291** |
| D4 le salon est grand et le salon est clair | **0,365** | 0,214 |

<div style="font-size:.84em; margin-top:6px;">

- En **comptages**, D4 gagne : il répète `salon` deux fois, alors qu'il ne parle pas d'animaux.
- En TF-IDF, **D3 gagne** : `salon` est banalisé (3 documents sur 4), `félin` retrouve son poids.
- C'est exactement le comportement attendu : la pondération corrige un classement trompeur.

</div>

---

### **Les limites de TF-IDF**

- **Synonymes** : `voiture` et `automobile` restent à distance
- **Plusieurs sens** : les deux sens d'`avocat` partagent une seule case
- **Ordre** : il n'est pas conservé
- **Mots inconnus** : ils sont ignorés
- **Corpus** : changer les documents change tous les poids

> TF-IDF donne un poids aux mots, il ne comprend pas leur sens.

---

### **Récapitulatif**

<div style="font-size:.86em;">

1. **TF** mesure la présence dans le document, **IDF** la rareté dans le corpus.
2. La convention scikit-learn est **lissée** : un mot présent partout garde un IDF de 1 — un **plancher**, pas un poids fort.
3. TF-IDF **accentue les écarts** ; il ne change l'ordre que quand un mot banal écrase un mot qui distingue.
4. Il reste **basé sur les mots** : synonymes, plusieurs sens et mots inconnus lui échappent.

</div>

<div style="margin-top:14px; padding:14px 18px; background:#f4f7ff; border-radius:10px; font-size:.92em;">
<strong>Question</strong> — Pourquoi un IDF calculé sur 4 documents ne doit-il pas être réutilisé tel quel sur un corpus de 10 000 documents ?
</div>

---

<!-- header: ⭐️ Des mots aux vecteurs -->

### **Un one-hot ne dit rien**

<div style="display:flex; gap:18px; font-size:.84em; margin-top:4px;">
<div style="flex:1;">

**Le one-hot**

Un vecteur de la taille du vocabulaire, avec un seul 1.

```
chat  = [1,0,0,0,0,...]
chien = [0,1,0,0,0,...]
pneu  = [0,0,0,1,0,...]
```

cos(chat, chien) = **0**<br/>
cos(chat, pneu) = **0**<br/>
Aucune information : tous les mots sont équidistants.

</div>
<div style="flex:1;">

**L'idée de base** (Firth, 1957)

> « You shall know a word by the company it keeps. »

Deux mots qui apparaissent **dans les mêmes contextes** ont un sens proche.

C'est tout le programme de Word2Vec : apprendre des vecteurs **à partir des voisinages**, sans dictionnaire.

<p style="font-size:.68em; color:#9aa4b8; margin-top:6px;">Mikolov et al. (2013), <em>Efficient Estimation of Word Representations in Vector Space</em>.</p>

</div>
</div>

---

### **La fenêtre glissante**

<p style="font-size:.86em; margin:2px 0 6px 0;">
<code>le(0) chat(1) dort(2) sur(3) canapé(4)</code> — fenêtre <em>k</em> = 2
</p>

<div style="display:flex; gap:18px; font-size:.84em;">
<div style="flex:1;">

**Cible : `dort` (position 2)**

Contexte = mots à une distance ≤ 2 :

`le` (0) · `chat` (1) · `sur` (3) · `canapé` (4)

→ 4 associations mot ↔ contexte :<br/>
(`dort`, `le`), (`dort`, `chat`), (`dort`, `sur`), (`dort`, `canapé`)

</div>
<div style="flex:1; background:#f4f7ff; border-radius:8px; padding:12px 14px;">

**Puis on décale**

Cible `le` (0) : contexte `chat`, `dort` (bornes !)<br/><br/>
Cible `chat` (1) : contexte `le`, `dort`, `sur`<br/><br/>
… et ainsi de suite sur tout le corpus.

</div>
</div>

<div style="margin-top:10px; padding:10px 14px; background:#fff4e5; border-left:4px solid #d97706; border-radius:6px; font-size:.84em;">
La fenêtre est un <strong>hyperparamètre</strong> : petite = relations syntaxiques, grande = thèmes.
</div>

---

### **Deux façons d'apprendre : CBOW et Skip-gram**

<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:8px; font-size:.84em;">

<div style="background:#f4f7ff; border-radius:10px; padding:14px 16px;">
<strong>CBOW</strong> — prédire le centre depuis le contexte

```
contexte : le, chat, sur, canapé
        ↓
cible    : dort
```

Rapide, efficace sur les mots fréquents.

</div>

<div style="background:#f4f7ff; border-radius:10px; padding:14px 16px;">
<strong>Skip-gram</strong> — prédire le contexte depuis le centre

```
cible    : dort
        ↓
contexte : le, chat, sur, canapé
```

Plus lent, meilleur sur les **mots rares**.

</div>

</div>

<div style="margin-top:12px; font-size:.84em; color:#4b5563;">
Les deux produisent la même chose : une matrice de vecteurs. Seul le sens des paires change.
</div>

---

### **Où sont les vecteurs ?**

<div style="font-size:.86em;">

Chaque mot possède une ligne dans la <strong>matrice d'entrée W</strong> (taille <em>|V| × d</em>) : c'est elle qui contient les embeddings.

</div>

$$
h=\frac{1}{|C|}\sum_{w\in C} \mathbf{e}_w
\qquad\text{avec } C=\text{contexte}(w_t),\ w_t\notin C,\ |C|\leq 2k
$$

<div style="font-size:.78em; color:#4b5563; margin-top:2px;">
<em>e<sub>w</sub></em> = le vecteur du mot <em>w</em> (une ligne de W) · <em>w<sub>t</sub></em> = le mot central, la cible · <em>h</em> = le vecteur agrégé du contexte ·
|C| ≤ 2k parce qu'au premier mot de la phrase, la fenêtre ne contient que k voisins.
</div>

<div style="font-size:.84em; margin-top:6px;">

- **CBOW** : on moyenne les vecteurs du contexte pour former <em>h</em>, puis on calcule un score pour chaque mot du vocabulaire.
- **Skip-gram** : on part du vecteur du mot central et on calcule un score pour chaque mot du contexte.
- L'entraînement **ajuste W** : les mots réellement observés doivent obtenir un score élevé.

</div>

---

### **Combien ça coûte ?**

<div style="display:flex; gap:20px; font-size:.86em; margin-top:4px;">
<div style="flex:1;">

**Deux matrices**

- entrée : <em>|V| × d</em>
- sortie : <em>|V| × d</em>

10 000 mots × 100 dimensions → **2 × 10⁶ poids**

<div style="margin-top:8px; font-size:.92em; color:#4b5563;">
La <strong>ligne de la matrice d'entrée</strong> associée à un mot <em>est</em> son embedding : la couche intermédiaire n'est que la moyenne de ces lignes.
</div>

</div>
<div style="flex:1;">

**Ordres de grandeur**

- corpus : millions de mots
- dimension : 100 à 300 — compromis capacité / coût ; au-delà, les gains deviennent marginaux
- vocabulaire : 10⁴ à 10⁶

</div>
</div>

<div style="margin-top:14px; padding:12px 16px; background:#fff4e5; border-left:4px solid #d97706; border-radius:6px; font-size:.86em;">
Un vocabulaire de 100 000 mots en 300 dimensions = <strong>60 millions</strong> de paramètres, pour deux matrices.
Et pour chaque paire, il faut calculer <em>|V|</em> scores : c'est ce <strong>coût de calcul</strong> que réduisent le negative sampling et le softmax hiérarchique (séance 6), pas le nombre de paramètres.
</div>

---

### **Ce que ça donne**

<div style="display:flex; gap:18px; align-items:center;">
<div style="flex:1;">

![width:430px](./images/word2vec-plan.svg)

</div>
<div style="flex:1; font-size:.84em;">

Après entraînement sur un gros corpus, les voisins de `chat` sont `chien`, `matou`, `félin` — avec des cosinus de 0,6 à 0,9.<br/><span style="color:#4b5563;">Même famille sur le modèle du TP : `félin` 0,72 · `chien` 0,62 · `chats` 0,62.</span>

Les thèmes se regroupent **sans qu'on les ait jamais nommés**.

</div>
</div>

<div style="margin-top:10px; padding:10px 14px; background:#fff4e5; border-left:4px solid #d97706; border-radius:6px; font-size:.84em;">
Attention : c'est une similarité <strong>de contextes</strong>, pas du « sens ».
<code>chaud</code> et <code>froid</code> sont proches (mêmes contextes) ; <code>canapé</code> et <code>sofa</code> aussi.
</div>

---

### **Lire un espace d'embeddings**

<div style="display:flex; gap:14px; align-items:flex-start;">
<div style="flex:1.05;">

![width:470px](./images/analogie-embedding-space.png)

</div>
<div style="flex:1; font-size:.76em;">

**1.** Chaque mot est un **vecteur tracé depuis l'origine** (MAN = `homme`, WOMAN = `femme`, KING = `roi`, QUEEN = `reine`).

**2.** Les flèches violettes « Gender » sont **identiques** : MAN→WOMAN et KING→QUEEN.

**3.** Les flèches orange « Royalty » sont **identiques** : MAN→KING et WOMAN→QUEEN.

**4.** Les quatre points forment un **parallélogramme** :

<code style="font-size:1.05em;">QUEEN = KING + (WOMAN − MAN)</code>

</div>
</div>

<p style="text-align:center; font-size:.8em; color:#4b5563; margin-top:4px;">
Un vecteur différence n'est pas un mot : c'est un <strong>sens</strong> — et il se réutilise.
</p>

<p style="font-size:.6em; color:#9aa4b8; margin-top:0;">Figure : schéma de @akshay_pachaar, repris tel quel avec son crédit d'auteur.</p>

---

### **Ce que ça vaut vraiment**

- **Ce qui marche** : `reine` sort en tête pour `roi − homme + femme`
- **Ce qui échoue** : `paris − france + italie` peut donner `espagne`
- **Le chiffre** : cos(`reine−roi`, `femme−homme`) = **0,37** sur notre modèle
- **Pourquoi** : un petit corpus donne des vecteurs moins fiables

> Une analogie réussie ne prouve pas que le modèle a compris.

---

### **D'un mot à un document**

<div style="font-size:.86em;">

Un mot a maintenant un vecteur. Mais une **phrase**, un **paragraphe**, un **document** en ont-ils un ?

</div>

<div style="display:flex; gap:18px; margin-top:8px; font-size:.84em;">
<div style="flex:1; background:#f4f7ff; border-radius:8px; padding:12px 14px;">
<strong>Pooling</strong><br/>
Moyenner les vecteurs des mots du document.<br/>
Simple — mais l'ordre et les relations entre mots disparaissent.
</div>
<div style="flex:1; background:#f4f7ff; border-radius:8px; padding:12px 14px;">
<strong>Encodeur de phrases</strong><br/>
Un modèle entraîné pour produire <em>directement</em> un vecteur de phrase.<br/>
C'est ce que fait <code>sentence-transformers</code> (séance 6).
</div>
</div>

<div style="margin-top:14px; padding:12px 16px; border:1.5px dashed #3d65f6; border-radius:8px; font-size:.88em;">
C'est <strong>ce</strong> vecteur-là qui servira à comparer des phrases entières — pas les vecteurs de mots isolés.<br/>
Tant que ce maillon n'est pas vu, la comparaison de documents reste une boîte noire.
</div>

---

<!-- header: ⭐️ Limites -->

### **Cinq limites, un même mur**

| Limite | Symptôme | Ce qu'il faudrait |
|---|---|---|
| **Lexical** (BoW, TF-IDF) | `voiture` / `automobile` → cosinus 0 | des vecteurs appris |
| **Polysémie** | `avocat` = fruit **et** métier, un seul vecteur | un vecteur **par contexte** |
| **Ordre** | `le chien mord l'homme` ≈ `l'homme mord le chien` | modéliser la séquence |
| **Hors vocabulaire** | un mot absent n'a <em>aucun</em> vecteur | des sous-mots (fastText), un vrai encodeur |
| **Expression** | `animal de compagnie` : le sens n'est pas la somme des mots | un encodeur de phrases |

<div style="margin-top:12px; padding:10px 14px; background:#f4f7ff; border-radius:8px; font-size:.84em;">
Word2Vec <strong>atténue</strong> la première ligne, sans la supprimer. Les suivantes demandent de regarder <strong>la phrase entière</strong>, pas le mot isolé.
</div>

---

### **Un vecteur par contexte**

- **Fruit** : « L'avocat mûr tombe de l'arbre. »
- **Métier** : « L'avocat plaide au tribunal. »
- **Word2Vec** : un seul vecteur pour `avocat`, les deux sens mélangés
- **BERT** : un vecteur différent dans chaque phrase

> Le contexte sert à choisir le bon sens — c'est l'objet de la séance 6.

---

### **Les trois façons de représenter un texte**

| | Ce qu'elle garde | Ce qu'elle perd | Coût |
|---|---|---|---|
| **Comptages (BoW)** | quels mots, combien de fois | l'ordre, les synonymes | très faible |
| **TF-IDF** | les mots qui distinguent | l'ordre, les synonymes | faible |
| **Word2Vec** | le sens approximatif | l'ordre, la précision | moyen |

<div style="margin-top:12px; font-size:.86em;">

**À retenir** : on ne remplace pas une méthode par une autre — on choisit celle qui correspond à la question posée.

</div>

<div style="margin-top:10px; padding:10px 14px; background:#f4f7ff; border-radius:8px; font-size:.84em;">
Une recherche par mots-clés exacts ? BoW ou TF-IDF suffit.
Une recherche où l'utilisateur écrit autrement que le document ? Il faut Word2Vec.
</div>

---

### **Exercice : trois phrases, trois vecteurs**

<p style="font-size:.84em; color:#4b5563; margin:2px 0 6px 0;">Corpus de trois phrases :</p>

<div style="font-size:.84em; line-height:1.5;">
<code>D1</code> le chat dort sur le canapé<br/>
<code>D2</code> le chien dort sur le tapis<br/>
<code>D3</code> un félin se repose sur le sofa
</div>

<div style="display:flex; gap:16px; font-size:.82em; margin-top:10px;">
<div style="flex:1;">

**1.** Vectoriser en comptages.

**2.** Calculer le cosinus entre D1 et D2, puis entre D1 et D3.

</div>
<div style="flex:1;">

**3.** Refaire le calcul en TF-IDF.

**4.** Expliquer pourquoi D3 change de place.

</div>
</div>

<div style="margin-top:10px; padding:10px 14px; border:1.5px dashed #3d65f6; border-radius:8px; font-size:.84em;">
Attendu : D1 et D2 se ressemblent (mêmes mots outils, <code>dort</code> en commun). D3 parle de la même chose sans partager un seul mot de contenu — les comptages ne peuvent pas le voir.
</div>

---

### **Ce qu'il faut savoir refaire à la main**

<div style="font-size:.86em; line-height:1.6;">

- **1.** Compter les occurrences et construire la matrice documents × termes.
- **2.** Calculer un IDF : `log(N / df)` — et dire pourquoi il monte quand le mot est rare.
- **3.** Calculer un cosinus entre deux vecteurs, y compris le cas du vecteur nul.
- **4.** Remplir une matrice de Levenshtein sur 4 × 4 cases.
- **5.** Trouver les voisins d'un mot dans un fichier de vecteurs.

</div>

<div style="margin-top:12px; padding:10px 14px; background:#f4f7ff; border-radius:8px; font-size:.86em;">
Si ces cinq gestes sont acquis, la suite (phrase, document, recherche) n'est plus qu'une combinaison de ce que vous savez déjà.
</div>

---

### **La carte du cours**

![width:820px](./images/pipeline-cours5.svg)

- **Levenshtein** : compare les caractères, sans dictionnaire
- **BoW / TF-IDF** : comptent les mots et donnent un poids aux mots rares
- **Word2Vec** : rapproche les mots employés dans les mêmes contextes
- **Toutes** perdent quelque chose : ordre, synonymes ou mots inconnus

> Il n'existe pas de « meilleure représentation » : il existe une représentation adaptée à une question, avec un prix connu.

---

### **Trois situations, trois choix**

<p style="font-size:.84em; margin:0 0 6px 0;">
Pour chacune, quelle représentation choisissez-vous — et quelle limite acceptez-vous ?
</p>

<div style="display:flex; flex-direction:column; gap:9px; font-size:.82em;">
<div style="background:#f4f7ff; border-radius:8px; padding:10px 14px;">
<strong>1.</strong> Chercher <code>voiture</code> dans un catalogue qui n'écrit que <code>automobile</code>.
</div>
<div style="background:#f4f7ff; border-radius:8px; padding:10px 14px;">
<strong>2.</strong> Retrouver les documents où <code>avocat</code> désigne le fruit, pas le métier.
</div>
<div style="background:#f4f7ff; border-radius:8px; padding:10px 14px;">
<strong>3.</strong> Répondre à une question dont <em>aucun</em> mot n'appartient au vocabulaire du corpus.
</div>
</div>

<p style="font-size:.8em; color:#4b5563; margin-top:10px;">
Attendu : une représentation nommée (BoW, TF-IDF, Word2Vec, encodeur de phrase), une justification, et la limite assumée.
</p>

---

### **Le TP : 3 blocs, 1 heure**

<div style="display:flex; gap:16px; font-size:.82em; margin-top:4px;">
<div style="flex:1; background:#f4f7ff; border-radius:10px; padding:12px 14px;">
<strong>Bloc 1 · 15 min</strong><br/>
Normaliser, tokeniser, filtrer les stop words. Mesurer l'effet de chaque choix.
</div>
<div style="flex:1; background:#f4f7ff; border-radius:10px; padding:12px 14px;">
<strong>Bloc 2 · 20 min</strong><br/>
BoW → TF-IDF → cosinus. Classer une requête, provoquer un vecteur nul.
</div>
<div style="flex:1; background:#f4f7ff; border-radius:10px; padding:12px 14px;">
<strong>Bloc 3 · 12 min</strong><br/>
Embeddings pré-calculés : voisins, analogie, un échec à expliquer.
</div>
</div>

<p style="font-size:.76em; color:#4b5563; margin-top:8px;">
Total des blocs : 47 min — les <strong>13 minutes restantes</strong> sont consacrées à la lecture des consignes, aux erreurs d'exécution et aux questions.
</p>

<div style="margin-top:14px; font-size:.84em;">

**À savoir faire en sortant**

- expliquer pourquoi <code>voiture</code> et <code>automobile</code> ont un cosinus de 0 en TF-IDF
- dire ce qu'un `fit` fige, et ce qu'un `transform` ignore
- choisir entre comptage et vecteurs denses pour une tâche donnée

</div>

<p style="text-align:center; margin-top:14px; font-size:.9em; color:#3d65f6;">
<strong>→ Place au TP.</strong>
</p>
