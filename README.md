# capture
Recupération fichier Capture corrompu
# Capture Recovery

> Reverse engineering framework for Capture 2024 project files (`.c2p`).

Capture Recovery est un framework Python destiné à l'analyse, la compréhension et la récupération des fichiers **Capture** (`.c2p`).

Le projet a pour objectif de reconstruire progressivement la structure interne du format de fichier sans disposer de sa spécification officielle.

---

# Objectifs

- Comprendre le format binaire `.c2p`
- Détecter automatiquement les structures de données
- Identifier les objets Capture (Fixtures, Universes, Cameras, Layers, etc.)
- Reconstruire un projet Capture à partir d'un fichier
- Récupérer des données depuis des fichiers corrompus
- Fournir une base open source pour le reverse engineering de Capture

---

# Fonctionnalités actuelles

## Détection

- Signatures binaires
- Chaînes ASCII
- Chaînes UTF-16
- Entiers
- Nombres flottants

## Analyse

- Détection de structures
- Analyse de motifs
- Analyse d'entropie
- Détection de pointeurs
- Analyse de blocs
- Détection de tableaux de flottants

## Infrastructure

- BinaryReader
- DetectorPipeline
- DetectionIndex
- Report
- Export JSON
- Architecture modulaire
- Tests unitaires

---

# Architecture

```
                .c2p
                  │
                  ▼
          BinaryReader
                  │
                  ▼
         DetectorPipeline
                  │
                  ▼
            Detection[]
                  │
                  ▼
          DetectionIndex
                  │
                  ▼
             Analyzers
                  │
                  ▼
               Report
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
      JSON               HTML
```

---

# Structure du projet

```
capture-recovery/

├── docs/
├── samples/
├── src/
│   └── capture_recovery/
│       ├── analyzers/
│       ├── detectors/
│       ├── diff/
│       ├── exporters/
│       ├── indexes/
│       ├── inference/
│       ├── models/
│       ├── scanners/
│       ├── binary_reader.py
│       └── structure_parser.py
│
├── tests/
│
├── capture_scan.py
├── pyproject.toml
└── README.md
```

---

# Installation

```bash
git clone https://github.com/hennautstephan-pixel/capture.git

cd capture

python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -e .
```

---

# Utilisation

Scanner un projet Capture :

```bash
python capture_scan.py samples/Structure.c2p
```

À terme :

```bash
python capture_diff.py \
    samples/Vide.c2p \
    samples/Projo.c2p
```

---

# État du projet

Le projet est en développement actif.

Fonctionnalités déjà disponibles :

- Binary Reader
- Détecteurs
- Analyseurs
- Export JSON
- Tests unitaires

Fonctionnalités en cours :

- Memory Map
- Region Builder
- Diff Engine
- Knowledge Engine

Fonctionnalités prévues :

- Reconstruction des objets Capture
- Export HTML interactif
- Graphe mémoire
- Signature Database
- Analyse automatique des versions de Capture

---

# Roadmap

## v0.1

- Infrastructure
- Détecteurs
- Analyseurs
- Tests
- Export JSON

## v0.2

- MemoryMap
- RegionBuilder
- capture_diff
- HTML Report

## v0.5

- Signature Engine
- Pointer Graph
- Matrix Detection
- Object Tables

## v1.0

- Reconstruction d'un projet Capture
- Détection automatique des objets
- Export complet
- Documentation

---

# Documentation

Le dossier `docs/` contient :

- FORMAT.md
- REVERSE_ENGINEERING.md
- ROADMAP.md

---

# Tests

Lancer tous les tests :

```bash
pytest
```

Avec couverture :

```bash
pytest --cov=src
```

---

# Philosophie

Capture Recovery ne cherche pas à modifier les fichiers Capture.

Le projet a pour objectif de :

- comprendre le format ;
- documenter les découvertes ;
- récupérer les données ;
- construire une base de connaissances ouverte.

Toutes les hypothèses sont validées expérimentalement à partir de fichiers de référence.

---

# Contribuer

Les contributions sont les bienvenues.

Vous pouvez participer en :

- proposant des améliorations ;
- ouvrant une Issue ;
- soumettant une Pull Request ;
- partageant des fichiers `.c2p` de test ;
- documentant le format.

---

# Licence

À définir.

Une licence MIT est envisagée.

---

# Auteur

**Stéphan Hennaut**

Projet open source consacré au reverse engineering des fichiers Capture (`.c2p`).