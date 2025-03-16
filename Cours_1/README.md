# Présentation Marp avec thème Beam

Ce projet contient une présentation créée avec [Marp](https://marp.app/) (Markdown Presentation Ecosystem) sur le thème du datamining. Le thème utilisé est [Beam](https://rnd195.github.io/marp-community-themes/theme/beam.html), qui offre un design élégant inspiré des présentations LaTeX Beamer.

## 📁 Structure du projet

```
marp-presentation/
├── presentation.md          # Fichier principal de la présentation
├── themes/
│   └── beam.css             # Thème Beam
└── README.md                # Ce fichier
```

## 🚀 Comment l'utiliser

### Prérequis

Pour utiliser cette présentation, vous aurez besoin de :

1. [Node.js](https://nodejs.org/) (recommandé)
2. Le CLI Marp ou une extension Marp pour votre éditeur

### Installation

1. **Installer Marp CLI** (globalement):

```bash
npm install -g @marp-team/marp-cli
```

2. **Alternative: Utiliser une extension pour votre éditeur**:
   - VS Code: [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
   - JetBrains (WebStorm, IntelliJ, etc.): [Plugin Marp](https://plugins.jetbrains.com/plugin/16387-marp)

### Générer une présentation

Pour générer une présentation au format PDF:

```bash
marp --theme ./themes/beam.css presentation.md --pdf
```

Pour générer une présentation au format HTML:

```bash
marp --theme ./themes/beam.css presentation.md --html
```

Pour générer des diapositives au format PPTX:

```bash
marp --theme ./themes/beam.css presentation.md --pptx
```

### Présentation en mode serveur

Pour visualiser la présentation en temps réel avec rafraîchissement automatique:

```bash
marp --theme ./themes/beam.css presentation.md --watch
```

## 🎨 Personnalisation du thème

Le thème Beam offre plusieurs classes CSS spéciales que vous pouvez utiliser:

- `<!-- _class: title -->` - Pour la diapositive de titre
- `<!-- _class: section -->` - Pour les diapositives de section
- `<!-- _class: toc -->` - Pour la table des matières
- `<!-- _class: default -->` - Style standard
- `<!-- _class: references -->` - Pour les références bibliographiques
- `<!-- _class: end -->` - Pour la dernière diapositive

### Éléments de mise en page

- Utilisez `<div class="definition">` pour encadrer des définitions
- Utilisez `<div class="alert">` pour des alertes/informations importantes
- Utilisez `<div class="example">` pour des exemples concrets
- Utilisez `<div class="two-columns">` pour créer deux colonnes
- Utilisez `<div class="columns-3">` pour créer trois colonnes
- Utilisez `<div class="columns-2">` pour créer deux colonnes

### Images

Pour les images d'arrière-plan:

```markdown
![bg right:40% h:300px](image.jpg)
```

Pour les images standard avec largeur spécifique:

```markdown
![w:500px](image.jpg)
```

## 📝 Comment modifier la présentation

Ouvrez le fichier `presentation.md` dans votre éditeur préféré et modifiez le contenu Markdown. Les métadonnées de la présentation se trouvent en haut du fichier:

```yaml
---
marp: true
theme: beam
paginate: true
size: 16:9
title: Cours de Datamining - Licence Informatique
author: Votre Nom
date: 2023-10-01
header: "**Cours de Datamining**"
footer: "Licence Informatique - 2023"
---
```

## 📚 Ressources utiles

- [Documentation officielle de Marp](https://marpit.marp.app/markdown)
- [Galerie de thèmes Marp Community](https://github.com/rnd195/marp-community-themes)
- [Documentation du thème Beam](https://rnd195.github.io/marp-community-themes/theme/beam.html)
- [Cheatsheet Markdown](https://www.markdownguide.org/cheat-sheet/)
