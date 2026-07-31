# Capture Recovery

> **Open-source reverse engineering framework for Capture™ project files (`.c2p`)**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Tests](https://img.shields.io/badge/Tests-1523%2B-success.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Active%20Development-green.svg)

---

# Overview

Capture Recovery est un framework Python open source consacré à l'analyse, la compréhension et la reconstruction des fichiers de projets **Capture™** (`.c2p`).

Contrairement à un simple éditeur ou convertisseur de fichiers, le projet poursuit un objectif beaucoup plus ambitieux : **comprendre le format interne des fichiers Capture sans disposer de leur spécification officielle**.

Le logiciel développe progressivement une connaissance du format grâce à l'analyse de projets réels, à l'observation des différences entre fichiers et à un moteur d'inférence capable de déduire automatiquement les propriétés des objets.

L'objectif final est de disposer d'un moteur capable de :

- comprendre la structure complète d'un fichier `.c2p` ;
- reconstruire un projet valide à partir de données binaires ;
- récupérer des informations depuis des fichiers partiellement corrompus ;
- documenter le format de manière reproductible ;
- constituer une base de connaissances ouverte autour du format Capture.

---

# Pourquoi ce projet ?

Les fichiers Capture utilisent un format binaire propriétaire qui n'est pas documenté publiquement.

Lorsqu'un projet devient corrompu, il n'existe aujourd'hui pratiquement aucun outil permettant de :

- récupérer une partie des données ;
- comprendre l'origine du problème ;
- reconstruire automatiquement les objets encore présents ;
- comparer deux versions d'un même projet ;
- documenter précisément le contenu du fichier.

Capture Recovery est né pour répondre à ces besoins.

Le projet ne repose pas sur une spécification interne ni sur une rétro-ingénierie invasive : toutes les découvertes proviennent exclusivement de l'observation et de l'analyse de fichiers réels.

---

# Philosophie

Le projet repose sur plusieurs principes fondamentaux.

## 1. Expérimentation

Aucune hypothèse n'est considérée comme vraie tant qu'elle n'a pas été validée expérimentalement sur plusieurs fichiers.

Chaque découverte doit pouvoir être reproduite.

---

## 2. Architecture modulaire

Chaque composant possède une responsabilité clairement définie.

Exemples :

- BinaryReader
- StructureParser
- DiffEngine
- PropertyDiscoveryEngine
- CorrelatorRegistry
- ConstraintMerger
- ConstraintValidator
- ConfidenceAggregator
- ReconstructionEngine

Cette séparation permet de faire évoluer le logiciel sans remettre en cause l'ensemble de l'architecture.

---

## 3. Développement piloté par les tests

Le projet possède aujourd'hui plus de **1523 tests unitaires** couvrant les principaux composants.

Chaque nouvelle fonctionnalité est accompagnée de ses propres tests afin de garantir l'absence de régression.

Les tests ne servent pas uniquement à vérifier le code : ils documentent également le comportement attendu du framework.

---

## 4. Développement piloté par les données

Les tests unitaires garantissent la stabilité du logiciel.

Les véritables fichiers `.c2p`, stockés dans le dossier `samples/`, permettent quant à eux de mesurer les performances du moteur sur des projets réels.

À terme, chaque évolution sera évaluée à partir de deux critères :

- les tests unitaires doivent rester verts ;
- les performances sur le corpus de projets doivent progresser.

Cette approche garantit une amélioration continue du moteur de découverte.

---

# Objectifs

## Court terme

- Stabiliser l'architecture.
- Documenter le format.
- Développer les moteurs d'inférence.
- Identifier automatiquement les propriétés des objets.

## Moyen terme

- Reconstruire automatiquement les objets Capture.
- Développer une base de connaissances.
- Améliorer la récupération de fichiers corrompus.
- Générer des rapports détaillés d'analyse.

## Long terme

Le but final est de disposer d'un framework capable de reconstruire un projet Capture complet à partir d'un fichier binaire, même lorsque certaines parties du fichier sont endommagées.

Cette reconstruction devra être accompagnée d'un niveau de confiance mesurable et d'une explication des hypothèses retenues par le moteur.

---

# État actuel du projet

Le projet est actuellement dans une phase de développement avancée.

Les fondations de l'architecture sont désormais en place et les efforts se concentrent progressivement sur l'amélioration de l'intelligence du moteur.

Fonctionnalités disponibles :

- Lecture binaire avancée
- Analyse de structures
- Détection automatique de propriétés
- Corrélateurs spécialisés
- Fusion intelligente des contraintes
- Validation des contraintes
- Agrégation probabiliste de la confiance
- Infrastructure modulaire
- Suite de plus de **1523 tests unitaires**

Les prochaines étapes concernent principalement :

- le framework de benchmark ;
- la base de connaissances ;
- l'apprentissage automatique des propriétés ;
- l'amélioration de la reconstruction des projets Capture.

---

> Capture Recovery n'a pas vocation à remplacer Capture™.
>
> Son objectif est de comprendre, documenter et reconstruire les fichiers `.c2p` de manière transparente, reproductible et ouverte, afin de constituer une référence technique pour la communauté.

# Architecture générale

Capture Recovery est construit autour d'une architecture en pipeline.

Chaque composant possède une responsabilité unique et communique avec les composants suivants au moyen de structures de données immuables.

Cette architecture permet :

- une grande extensibilité ;
- un fort découplage des modules ;
- une excellente testabilité ;
- l'ajout de nouveaux moteurs d'analyse sans modifier les composants existants.

L'objectif est que chaque étape puisse évoluer indépendamment des autres.

---

# Vue d'ensemble

```
                               Capture Project (.c2p)
                                         │
                                         ▼
                                 BinaryReader
                                         │
                                         ▼
                                Structure Parser
                                         │
                                         ▼
                                  Binary Regions
                                         │
                                         ▼
                                  Diff Engine
                                         │
                                         ▼
                             Property Observations
                                         │
                                         ▼
                          Property Discovery Engine
                                         │
                 ┌───────────────────────┼────────────────────────┐
                 ▼                       ▼                        ▼
        Correlator Registry      Constraint Engine        Knowledge Engine
                 │                       │                        │
                 ▼                       ▼                        ▼
        Property Candidates      Validated Constraints      Learned Rules
                 └───────────────────────┼────────────────────────┘
                                         ▼
                              Object Reconstruction
                                         │
                                         ▼
                              Reconstructed Project
```

---

# Les différentes couches

Le framework est composé de plusieurs couches indépendantes.

```
+---------------------------------------------------------------+
|                     Reconstruction Layer                      |
+---------------------------------------------------------------+
|                     Knowledge Engine                          |
+---------------------------------------------------------------+
|                  Property Discovery Engine                    |
+---------------------------------------------------------------+
|                 Binary Analysis & Diff Engine                 |
+---------------------------------------------------------------+
|                       Binary Reader                           |
+---------------------------------------------------------------+
|                          .c2p File                            |
+---------------------------------------------------------------+
```

Chaque couche ajoute un niveau d'abstraction supplémentaire.

---

# 1. Binary Reader

Le BinaryReader constitue le point d'entrée du framework.

Il fournit une lecture sécurisée des données binaires :

- entiers signés ;
- entiers non signés ;
- flottants ;
- chaînes ASCII ;
- chaînes UTF-16 ;
- tableaux ;
- structures binaires.

Il masque totalement les détails liés à :

- l'endianness ;
- les offsets ;
- les conversions de types.

Tous les autres composants utilisent exclusivement cette API.

---

# 2. Structure Parser

Le Structure Parser transforme un simple flux d'octets en structures logiques.

Il identifie notamment :

- blocs ;
- régions ;
- tableaux ;
- structures répétitives ;
- signatures.

Cette étape ne tente pas encore d'interpréter les données.

Elle produit uniquement une représentation structurée du fichier.

---

# 3. Diff Engine

Le Diff Engine compare plusieurs projets Capture.

Son rôle est d'identifier :

- les offsets modifiés ;
- les valeurs ajoutées ;
- les valeurs supprimées ;
- les structures apparues ou disparues.

Cette étape est fondamentale pour le reverse engineering.

Elle permet d'associer les modifications effectuées dans Capture aux octets réellement modifiés dans le fichier.

---

# 4. Property Observation

Les différences observées sont transformées en observations.

Une observation représente un fait.

Par exemple :

```
Fixture
Offset 124
Value = 255
```

ou

```
Camera
Offset 88
Value = 90.0
```

Les observations constituent l'entrée du moteur de découverte.

---

# 5. Property Discovery Engine

Le Property Discovery Engine est le cœur du framework.

Il reçoit l'ensemble des observations et tente de découvrir automatiquement :

- le type de la propriété ;
- les contraintes associées ;
- le niveau de confiance.

Cette découverte repose sur plusieurs corrélateurs indépendants.

---

# Les corrélateurs

Chaque corrélateur possède une spécialité.

Exemple :

```
BooleanCorrelator
```

Détecte les valeurs booléennes.

```
IntegerCorrelator
```

Détecte les entiers.

```
NumericCorrelator
```

Détecte les types numériques.

```
EnumCorrelator
```

Détecte les ensembles finis de valeurs.

```
RangeCorrelator
```

Détecte les bornes minimales et maximales.

```
StepCorrelator
```

Détecte les incréments réguliers.

```
BitmaskCorrelator
```

Détecte les masques binaires.

Chaque corrélateur fonctionne indépendamment des autres.

Cette approche facilite énormément l'ajout de nouvelles heuristiques.

---

# Constraint Engine

Les contraintes découvertes sont ensuite :

1. fusionnées ;
2. validées ;
3. simplifiées ;
4. pondérées.

Les principaux composants sont :

```
ConstraintMerger
```

Fusionne les contraintes compatibles.

```
ConstraintValidator
```

Détecte les incompatibilités.

```
ConfidenceAggregator
```

Calcule une confiance globale à partir des différentes preuves.

Cette séparation rend les algorithmes beaucoup plus simples à maintenir.

---

# Knowledge Engine

Le Knowledge Engine représente la prochaine grande évolution du projet.

Il aura pour mission de mémoriser automatiquement les découvertes effectuées sur des centaines de projets Capture.

Par exemple :

- offsets fréquemment observés ;
- types les plus probables ;
- plages de valeurs ;
- dépendances entre propriétés.

L'objectif est que le logiciel améliore progressivement la qualité de ses inférences.

---

# Reconstruction Engine

Le Reconstruction Engine exploitera toutes les informations produites par les couches précédentes.

Il devra être capable de :

- reconstruire un objet Capture ;
- retrouver ses propriétés ;
- restaurer des valeurs manquantes ;
- générer une représentation exploitable du projet.

Cette couche constitue l'aboutissement du pipeline.

---

# Pourquoi cette architecture ?

Plusieurs objectifs ont guidé cette conception.

## Découplage

Chaque composant est indépendant.

Une amélioration locale ne remet pas en cause l'ensemble du framework.

---

## Extensibilité

L'ajout d'un nouveau corrélateur ne nécessite pas de modifier le moteur.

Il suffit de l'enregistrer dans le registre.

---

## Testabilité

Chaque composant peut être testé individuellement.

C'est ce qui permet aujourd'hui au projet de disposer de plus de **1500 tests unitaires** couvrant les différents niveaux de l'architecture.

---

## Évolutivité

Les futures évolutions (Knowledge Engine, Benchmark Framework, apprentissage automatique) pourront être intégrées sans modifier les fondations du logiciel.

Cette architecture a été pensée pour accompagner la croissance du projet sur plusieurs années.

# Structure du projet

Capture Recovery suit une architecture modulaire.

Chaque dossier possède une responsabilité clairement définie.

L'objectif est que le projet puisse évoluer pendant plusieurs années sans devenir difficile à maintenir.

---

# Vue générale

```text
capture-recovery/
│
├── docs/
├── samples/
├── scripts/
├── src/
│   └── capture_recovery/
│       ├── benchmark/
│       ├── binary/
│       ├── detectors/
│       ├── diff/
│       ├── discovery/
│       ├── exporters/
│       ├── inference/
│       ├── knowledge/
│       ├── models/
│       ├── reconstruction/
│       ├── scanners/
│       ├── utils/
│       └── version.py
│
├── tests/
│
├── pyproject.toml
├── pytest.ini
├── README.md
└── LICENSE
```

---

# docs/

Le dossier **docs** contient toute la documentation technique.

Exemples :

```
FORMAT.md
```

Description progressive du format `.c2p`.

```
REVERSE_ENGINEERING.md
```

Méthodologie employée.

```
ROADMAP.md
```

Feuille de route.

```
ARCHITECTURE.md
```

Description détaillée de l'architecture interne.

Ce dossier est destiné autant aux développeurs qu'aux personnes souhaitant comprendre le format Capture.

---

# samples/

Le dossier **samples** est l'un des éléments les plus importants du projet.

Il contient un ensemble de projets Capture servant de corpus de référence.

Par exemple :

```
Vide.c2p
```

Projet minimal.

```
Fixture.c2p
```

Un seul projecteur.

```
MovingHead.c2p
```

Projecteurs automatiques.

```
Hospitaliens.c2p
```

Projet réel utilisé comme benchmark.

Ces fichiers servent à :

- valider les hypothèses ;
- comparer plusieurs versions du moteur ;
- mesurer les performances ;
- enrichir la base de connaissances.

Aucun développement ne devrait être effectué sans validation sur ce corpus.

---

# src/

Le dossier **src** contient tout le code source.

Toutes les fonctionnalités du framework sont regroupées dans le package :

```
capture_recovery
```

---

# benchmark/

Le framework de benchmark.

Responsabilités :

- charger automatiquement les projets du dossier samples ;
- exécuter le pipeline complet ;
- mesurer les performances ;
- produire des statistiques ;
- générer des rapports.

Modules prévus :

```
BenchmarkRunner
```

```
BenchmarkStatistics
```

```
BenchmarkResult
```

```
BenchmarkReport
```

```
SampleLoader
```

---

# binary/

Cette couche fournit les abstractions de lecture binaire.

Elle masque complètement :

- les offsets ;
- l'endianness ;
- les conversions de types ;
- la lecture sécurisée.

Les autres composants ne manipulent jamais directement les octets.

---

# detectors/

Les détecteurs identifient des structures élémentaires.

Exemples :

- chaînes ASCII ;
- UTF-16 ;
- flottants ;
- entiers ;
- tableaux ;
- pointeurs ;
- signatures.

Ils travaillent uniquement sur les données binaires.

Ils ne connaissent pas la signification des objets Capture.

---

# diff/

Le moteur de comparaison.

Il compare plusieurs fichiers Capture.

Il identifie :

- les offsets modifiés ;
- les structures apparues ;
- les structures supprimées ;
- les différences de contenu.

Le Diff Engine constitue la principale source d'informations pour le moteur de découverte.

---

# discovery/

Le cœur du framework.

Il transforme les observations en connaissances.

On y trouve notamment :

```
PropertyDiscoveryEngine
```

```
CorrelatorRegistry
```

```
BooleanCorrelator
```

```
IntegerCorrelator
```

```
NumericCorrelator
```

```
EnumCorrelator
```

```
RangeCorrelator
```

```
StepCorrelator
```

```
BitmaskCorrelator
```

ainsi que

```
ConstraintMerger
```

```
ConstraintValidator
```

```
ConfidenceAggregator
```

Cette couche est entièrement indépendante du format Capture.

Elle peut être réutilisée pour d'autres formats binaires.

---

# exporters/

Les exporteurs convertissent les résultats.

Formats prévus :

- JSON
- Markdown
- HTML
- CSV

À terme, ils permettront également de générer des rapports interactifs.

---

# inference/

Cette couche contient les algorithmes d'inférence.

Elle regroupe les heuristiques permettant de transformer les observations en hypothèses.

À long terme, cette partie intégrera des modèles probabilistes plus avancés.

---

# knowledge/

La base de connaissances.

Elle mémorise progressivement :

- les signatures connues ;
- les offsets fréquents ;
- les plages observées ;
- les propriétés reconnues.

Cette couche permettra au logiciel d'améliorer automatiquement ses performances.

---

# models/

Les modèles représentent les objets manipulés par le framework.

Exemples :

- PropertyObservation
- PropertyCandidate
- DiscoveryResult
- BenchmarkResult

Ces classes sont volontairement simples.

Elles contiennent peu de logique métier.

---

# reconstruction/

Cette couche exploitera toutes les connaissances accumulées.

Objectifs :

- reconstruire un objet Capture ;
- restaurer les propriétés manquantes ;
- produire une représentation cohérente du projet.

À terme, cette couche deviendra probablement la plus complexe du framework.

---

# scanners/

Les scanners parcourent les fichiers binaires.

Ils alimentent ensuite les détecteurs et les moteurs d'analyse.

Ils représentent la première étape du pipeline.

---

# utils/

Fonctions utilitaires.

Exemples :

- conversions ;
- calculs ;
- statistiques ;
- helpers.

Aucune logique métier importante ne doit être placée ici.

---

# tests/

Le projet possède une suite importante de tests unitaires.

Chaque module possède son propre dossier de tests.

Par exemple :

```text
tests/

    benchmark/

    binary/

    diff/

    discovery/

    inference/

    reconstruction/
```

Chaque nouvelle fonctionnalité est accompagnée de ses propres tests.

L'objectif est de maintenir un niveau élevé de fiabilité tout au long du développement.

---

# Organisation générale

Le projet respecte une règle simple.

Les dépendances ne doivent aller que dans une seule direction.

```text
Benchmark

        ↑

Reconstruction

        ↑

Knowledge

        ↑

Discovery

        ↑

Diff Engine

        ↑

Binary Reader
```

Une couche ne doit jamais dépendre d'une couche située au-dessus d'elle.

Cette règle garantit la stabilité de l'architecture et facilite les évolutions futures.

# Property Discovery Engine

Le **Property Discovery Engine** est le cœur du framework Capture Recovery.

Il transforme une simple suite d'observations binaires en connaissances exploitables.

Contrairement à un analyseur classique qui applique des règles fixes, le moteur de découverte utilise plusieurs algorithmes spécialisés appelés **corrélateurs**.

Chaque corrélateur analyse les mêmes observations selon un point de vue différent.

Les résultats sont ensuite fusionnés afin de produire une hypothèse unique accompagnée d'un niveau de confiance.

---

# Vue d'ensemble

```
                    PropertyObservation
                              │
                              ▼
                  PropertyDiscoveryEngine
                              │
                              ▼
                     CorrelatorRegistry
                              │
      ┌───────────────────────┼────────────────────────┐
      ▼                       ▼                        ▼
Boolean               Numeric                 Enum
Integer               Range                   Step
Bitmask
      └───────────────────────┼────────────────────────┘
                              ▼
                    PropertyCandidate
                              │
                              ▼
                    ConstraintMerger
                              │
                              ▼
                  ConstraintValidator
                              │
                              ▼
                 ConfidenceAggregator
                              │
                              ▼
                     DiscoveryResult
```

---

# Principe

Chaque propriété observée est analysée indépendamment.

Exemple :

```
Fixture.Intensity

0
64
128
192
255
```

Plusieurs corrélateurs peuvent arriver simultanément aux conclusions suivantes :

```
IntegerCorrelator

↓

uint8
```

```
RangeCorrelator

↓

0..255
```

```
StepCorrelator

↓

step = 64
```

```
EnumCorrelator

↓

{0,64,128,192,255}
```

Le moteur ne choisit pas un seul résultat.

Toutes les hypothèses compatibles sont conservées puis fusionnées.

---

# PropertyObservation

Le moteur ne travaille jamais directement sur le fichier binaire.

Son entrée est une collection d'observations.

Une observation décrit un fait.

Par exemple :

```
Object

Fixture
```

```
Offset

124
```

```
Property

Intensity
```

```
Value

255
```

Toutes les analyses sont réalisées exclusivement à partir de ces observations.

---

# Correlator Registry

Le registre contient tous les corrélateurs disponibles.

Il permet au moteur de rester totalement extensible.

Exemple :

```
registry.register(BooleanCorrelator())

registry.register(IntegerCorrelator())

registry.register(EnumCorrelator())
```

L'ajout d'un nouveau corrélateur ne nécessite aucune modification du moteur.

---

# Les corrélateurs

Chaque corrélateur possède une responsabilité unique.

---

## BooleanCorrelator

Détecte les propriétés booléennes.

Exemple :

```
0

1

0

1

0
```

↓

```
Boolean
```

---

## IntegerCorrelator

Détermine si une propriété correspond à un entier.

Il détecte notamment :

- uint8
- int8
- uint16
- int16
- uint32
- int32

---

## NumericCorrelator

Détecte les propriétés numériques.

Il ne cherche pas à déterminer leur signification.

Son objectif est uniquement d'identifier la famille de type.

---

## EnumCorrelator

Recherche un ensemble fini de valeurs.

Exemple :

```
0

90

180

270
```

↓

```
Enum
```

---

## RangeCorrelator

Détermine les bornes observées.

Exemple :

```
minimum

0
```

```
maximum

255
```

↓

```
RangeConstraint
```

---

## StepCorrelator

Recherche un incrément régulier.

Exemple :

```
0

5

10

15

20
```

↓

```
StepConstraint(5)
```

---

## BitmaskCorrelator

Détecte les masques binaires.

Exemple :

```
1

2

4

8

16
```

↓

```
BitmaskConstraint
```

---

# PropertyCandidate

Chaque corrélateur retourne un PropertyCandidate.

Celui-ci contient :

- type supposé ;
- confiance ;
- contraintes ;
- nombre d'observations.

Il représente une hypothèse.

Plusieurs candidats peuvent être produits pour une même propriété.

---

# ConstraintMerger

Le rôle du ConstraintMerger est de fusionner les hypothèses compatibles.

Exemple :

```
uint8

Range

0..255
```

+

```
uint8

Step

1
```

↓

```
uint8

Range(0..255)

Step(1)
```

Aucune information n'est perdue.

---

# ConstraintValidator

Toutes les contraintes fusionnées sont ensuite validées.

Le validateur détecte notamment :

- plages incompatibles ;
- énumérations incompatibles ;
- bitmasks incompatibles ;
- pas incompatibles.

Les conflits sont enregistrés sans interrompre l'analyse.

---

# ConfidenceAggregator

Chaque corrélateur fournit un niveau de confiance.

Le ConfidenceAggregator combine ces informations afin de produire un score global.

Cette approche est plus robuste qu'un simple maximum.

Plusieurs preuves indépendantes renforcent naturellement la confiance finale.

---

# DiscoveryResult

Le résultat final contient :

- tous les PropertyCandidate retenus ;
- les statistiques d'analyse ;
- les informations de confiance.

Ce résultat devient ensuite l'entrée des couches suivantes :

- Knowledge Engine
- Reconstruction Engine
- Benchmark Framework

---

# Pourquoi cette approche ?

L'utilisation de plusieurs corrélateurs indépendants présente plusieurs avantages.

## Modularité

Chaque algorithme peut évoluer indépendamment.

---

## Testabilité

Chaque corrélateur possède sa propre suite de tests.

Aujourd'hui le moteur est couvert par plus de **1500 tests unitaires**.

---

## Extensibilité

Ajouter un nouveau corrélateur consiste simplement à :

1. créer une nouvelle classe ;
2. l'enregistrer dans le registre ;
3. ajouter ses tests.

Le reste du moteur ne change pas.

---

## Robustesse

Plusieurs corrélateurs peuvent confirmer simultanément une même hypothèse.

Cette redondance améliore la qualité des inférences et réduit les risques d'erreur.

---

# Évolutions prévues

Le moteur de découverte continuera à évoluer.

Les prochaines améliorations prévues sont notamment :

- pondération des corrélateurs ;
- apprentissage automatique des contraintes ;
- base de connaissances probabiliste ;
- explication détaillée des décisions ;
- détection automatique de nouveaux types de propriétés.

À terme, le Discovery Engine constituera un moteur générique capable d'être réutilisé pour l'analyse d'autres formats binaires que les seuls fichiers Capture.

# Reverse Engineering Pipeline

Le framework Capture Recovery repose sur un pipeline composé d'étapes indépendantes.

Chaque étape transforme les données produites par l'étape précédente.

Cette approche présente plusieurs avantages :

- composants fortement découplés ;
- excellente testabilité ;
- possibilité de remplacer un module sans modifier le reste du pipeline ;
- évolution progressive de l'intelligence du moteur.

---

# Vue d'ensemble

```
                   Capture Project (.c2p)

                            │
                            ▼

                     Binary Reader

                            │
                            ▼

                    Structure Parser

                            │
                            ▼

                      Binary Scanner

                            │
                            ▼

                       Diff Engine

                            │
                            ▼

                 Property Observations

                            │
                            ▼

               Property Discovery Engine

                            │
                            ▼

                  Constraint Processing

                            │
                            ▼

                  Knowledge Generation

                            │
                            ▼

                  Object Reconstruction

                            │
                            ▼

                     Benchmark Engine

                            │
                            ▼

                     Analysis Reports
```

---

# Étape 1 : Binary Reader

Le Binary Reader constitue la couche d'abstraction la plus basse.

Il est responsable de :

- la lecture sécurisée des données ;
- la gestion des offsets ;
- la conversion des types ;
- les vérifications de dépassement de limites ;
- l'accès uniforme au contenu du fichier.

Aucune logique métier n'est présente à ce niveau.

---

# Étape 2 : Structure Parser

Le Structure Parser tente d'identifier la structure générale du fichier.

Il détecte notamment :

- blocs ;
- régions ;
- tableaux ;
- séquences répétitives ;
- zones de texte ;
- signatures connues.

Cette étape produit une représentation logique du contenu binaire.

---

# Étape 3 : Binary Scanner

Le Scanner parcourt l'intégralité du fichier.

Il alimente ensuite les différents détecteurs.

Exemples :

- ASCII Detector
- UTF-16 Detector
- Integer Detector
- Float Detector
- Pointer Detector
- Signature Detector

Chaque détecteur produit ses propres découvertes.

---

# Étape 4 : Diff Engine

Le Diff Engine constitue l'un des piliers du projet.

Son principe est simple.

Deux projets Capture sont comparés.

Par exemple :

Projet A

```
Intensity = 50 %
```

Projet B

```
Intensity = 75 %
```

Le Diff Engine détermine exactement quels octets ont changé.

Ces différences deviennent ensuite des observations.

Cette approche permet d'associer progressivement chaque propriété Capture à une région du fichier.

---

# Étape 5 : Property Observations

Les différences sont converties en observations.

Une observation représente un fait.

Par exemple :

```
Object

Fixture
```

```
Offset

184
```

```
Property

Intensity
```

```
Observed value

255
```

Toutes les analyses du moteur reposent sur ces observations.

---

# Étape 6 : Discovery Engine

Le Discovery Engine est ensuite chargé d'interpréter les observations.

Il fait intervenir plusieurs corrélateurs indépendants.

Chaque corrélateur produit une hypothèse.

Exemple :

```
Integer
```

```
Range
```

```
Enum
```

```
Bitmask
```

Ces hypothèses sont ensuite fusionnées.

---

# Étape 7 : Constraint Processing

Cette étape comprend plusieurs composants.

## ConstraintMerger

Fusionne les contraintes compatibles.

---

## ConstraintValidator

Détecte les conflits.

---

## ConfidenceAggregator

Calcule une confiance globale.

Le résultat représente la meilleure hypothèse actuellement disponible.

---

# Étape 8 : Knowledge Generation

Les découvertes sont ensuite mémorisées.

Le futur Knowledge Engine enregistrera notamment :

- les offsets connus ;
- les types observés ;
- les plages ;
- les signatures ;
- les probabilités.

Le moteur deviendra progressivement capable d'apprendre.

---

# Étape 9 : Reconstruction

À partir des connaissances accumulées, le framework reconstruit progressivement les objets Capture.

Chaque objet est constitué de :

- ses propriétés ;
- leurs types ;
- leurs contraintes ;
- leur niveau de confiance.

L'objectif est de produire une représentation cohérente du projet.

---

# Étape 10 : Benchmark

Chaque projet analysé produit un ensemble de statistiques.

Par exemple :

- nombre d'objets ;
- nombre de propriétés ;
- nombre de contraintes ;
- confiance moyenne ;
- conflits détectés ;
- signatures inconnues.

Ces informations permettent de suivre les progrès du moteur.

---

# Rapports

Le framework pourra produire plusieurs formats de sortie.

## Console

Résumé rapide.

---

## JSON

Utilisable par d'autres outils.

---

## Markdown

Documentation automatique.

---

## HTML

Rapport interactif.

---

# Pourquoi un pipeline ?

Cette architecture présente plusieurs avantages.

## Simplicité

Chaque composant réalise une seule tâche.

---

## Réutilisabilité

Un module peut être utilisé indépendamment.

Par exemple :

- uniquement le Binary Reader ;
- uniquement le Diff Engine ;
- uniquement le Discovery Engine.

---

## Robustesse

Une erreur dans une étape ne remet pas en cause tout le pipeline.

Les étapes suivantes peuvent continuer à fonctionner avec les informations disponibles.

---

## Évolutivité

De nouvelles étapes pourront être ajoutées.

Par exemple :

```
AI Knowledge Engine
```

ou

```
Machine Learning Predictor
```

sans modifier les composants existants.

---

# Vision à long terme

À terme, Capture Recovery ne sera plus uniquement un logiciel de récupération de fichiers.

Il deviendra une plateforme complète de reverse engineering capable :

- d'apprendre automatiquement ;
- de documenter un format inconnu ;
- de reconstruire des structures complexes ;
- de comparer différentes versions d'un format ;
- d'expliquer les décisions prises par le moteur.

Cette architecture en pipeline est la base qui permettra ces évolutions.

# Knowledge Engine

Le **Knowledge Engine** constitue le cerveau de Capture Recovery.

Son rôle est de transformer les découvertes réalisées lors des analyses en connaissances réutilisables.

Contrairement aux autres composants du framework, qui travaillent uniquement sur le fichier actuellement analysé, le Knowledge Engine apprend progressivement à partir de l'ensemble des projets étudiés.

Chaque nouveau fichier Capture enrichit la base de connaissances.

L'objectif est simple :

> Plus le moteur analyse de projets, plus ses inférences deviennent fiables.

---

# Pourquoi un moteur de connaissances ?

Un reverse engineering classique applique toujours les mêmes règles.

Capture Recovery adopte une approche différente.

Au lieu de mémoriser uniquement des signatures binaires, le logiciel apprend progressivement :

- les objets fréquemment rencontrés ;
- les offsets connus ;
- les types observés ;
- les plages de valeurs ;
- les relations entre propriétés ;
- les probabilités d'apparition.

Cette approche permet au moteur d'améliorer continuellement ses performances.

---

# Architecture

```
                 Discovery Engine
                        │
                        ▼
             PropertyCandidate
                        │
                        ▼
               Knowledge Engine
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
 Known Types     Known Offsets    Known Rules
        ▼               ▼               ▼
               Knowledge Base
                        │
                        ▼
           Future Discoveries
```

---

# Fonctionnement

À chaque analyse, le moteur reçoit un ensemble de PropertyCandidate.

Par exemple :

```
Fixture

Offset 184

Type

float32

Confidence

0.99
```

Cette découverte est enregistrée.

Après plusieurs centaines d'analyses, la base pourra contenir :

```
Offset 184

Observations

684

Type

float32

Occurrence

99.8 %
```

Le moteur pourra alors utiliser cette information pour guider les futures analyses.

---

# Types de connaissances

Le Knowledge Engine mémorise plusieurs catégories d'informations.

## Types

Exemple :

```
Offset 96

Type

uint8
```

---

## Plages

```
Intensity

0..255
```

---

## Énumérations

```
Camera View

0

1

2

3
```

---

## Bitmasks

```
Flags

0x01

0x02

0x04

0x08
```

---

## Incréments

```
Rotation

Step

0.1
```

---

## Confiance

Chaque règle est associée à une confiance.

Exemple :

```
Offset 128

float32

Confidence

99.6 %
```

---

# Apprentissage

Le moteur n'enregistre jamais une seule observation comme une vérité.

Chaque découverte augmente progressivement un score.

Exemple :

Première observation

```
Offset 48

float32

1 observation
```

↓

```
Confiance

15 %
```

---

Après 500 projets

```
Offset 48

float32

497 observations
```

↓

```
Confiance

99.9 %
```

Les connaissances deviennent progressivement plus robustes.

---

# Relations entre propriétés

Le moteur ne mémorise pas uniquement des propriétés isolées.

Il pourra également apprendre des relations.

Par exemple :

```
Pan

↓

Toujours float32
```

```
Tilt

↓

Toujours float32
```

ou

```
Intensity

↓

Toujours compris entre

0

255
```

---

# Règles conditionnelles

Certaines propriétés n'existent que dans certains objets.

Le Knowledge Engine pourra mémoriser des règles comme :

```
Si

Object = Fixture

↓

Intensity existe
```

ou

```
Si

Object = Camera

↓

FOV existe
```

Ces règles permettront de réduire fortement les ambiguïtés.

---

# Statistiques

Chaque connaissance est accompagnée de statistiques.

Par exemple :

```
Occurrences

1542
```

```
Dernière observation

Capture 2024
```

```
Versions observées

2022

2023

2024
```

Ces informations permettront également d'étudier les évolutions du format Capture.

---

# Gestion des conflits

Deux observations peuvent être contradictoires.

Exemple :

```
Offset 184

float32
```

mais

```
Offset 184

uint32
```

Le moteur ne supprime pas une hypothèse.

Il conserve plusieurs possibilités avec leur probabilité respective.

Cette approche permettra à terme d'utiliser des méthodes probabilistes.

---

# Exploitation

Le Knowledge Engine sera utilisé par plusieurs composants.

## Discovery Engine

Pour améliorer les inférences.

---

## Reconstruction Engine

Pour reconstruire automatiquement des objets.

---

## Benchmark Framework

Pour mesurer l'évolution des connaissances.

---

## Documentation

Pour produire automatiquement une documentation du format Capture.

---

# Objectif à long terme

À terme, le Knowledge Engine devra être capable de répondre à des questions telles que :

- Quel est le type le plus probable de cette propriété ?
- Cette plage de valeurs est-elle habituelle ?
- Cet offset est-il connu ?
- Cette structure a-t-elle déjà été rencontrée ?
- Quelle est la probabilité que cette propriété corresponde à un angle ?
- Quelle version de Capture a introduit cette structure ?

Le framework ne sera alors plus seulement un analyseur binaire.

Il deviendra une véritable base de connaissances sur le format `.c2p`.

---

# Vision

À long terme, le Knowledge Engine constituera l'élément central du projet.

Les détecteurs, corrélateurs et moteurs de reconstruction produiront des connaissances.

Le Knowledge Engine les organisera, les validera et les enrichira progressivement.

L'objectif ultime est qu'après l'analyse de plusieurs milliers de projets Capture, le framework soit capable de reconnaître automatiquement la majorité des structures du format, d'expliquer ses décisions et d'améliorer continuellement ses performances sans remettre en cause son architecture.

# Benchmark Framework

À partir de cette version du projet, le développement de Capture Recovery ne repose plus uniquement sur les tests unitaires.

Le framework introduit une seconde méthode de validation :

**l'analyse automatique d'un corpus de projets Capture réels**.

Les fichiers présents dans le dossier `samples/` deviennent la référence permanente du projet.

Chaque évolution du moteur pourra être évaluée objectivement.

---

# Pourquoi un Benchmark ?

Les tests unitaires répondent à une seule question :

> Le code fonctionne-t-il comme prévu ?

Le Benchmark répond à une question beaucoup plus importante :

> Le moteur est-il réellement meilleur qu'avant ?

Cette distinction est essentielle.

Un algorithme peut réussir tous ses tests tout en étant incapable d'améliorer la reconstruction de vrais projets Capture.

Le Benchmark mesure précisément cette amélioration.

---

# Principe

Le Benchmark analyse automatiquement tous les fichiers présents dans :

```
samples/
```

Chaque projet est traité indépendamment.

Les résultats sont ensuite regroupés afin de produire des statistiques globales.

```
samples/

    Projet1.c2p

    Projet2.c2p

    Projet3.c2p

            │

            ▼

      Benchmark Runner

            │

            ▼

    Individual Results

            │

            ▼

  Benchmark Statistics

            │

            ▼

     Benchmark Report
```

---

# Objectifs

Le Benchmark poursuit plusieurs objectifs.

## Validation

Vérifier que les évolutions améliorent réellement le moteur.

---

## Régression

Détecter immédiatement une baisse de performance.

---

## Comparaison

Comparer deux versions du framework.

---

## Mesure

Fournir des indicateurs objectifs.

---

## Documentation

Produire automatiquement des rapports exploitables.

---

# Architecture

Le Benchmark est constitué de plusieurs composants.

```
Sample Loader

        │

        ▼

Benchmark Runner

        │

        ▼

Benchmark Result

        │

        ▼

Benchmark Statistics

        │

        ▼

Benchmark Report
```

Chaque composant possède une responsabilité unique.

---

# Sample Loader

Le Sample Loader découvre automatiquement tous les projets Capture présents dans le dossier :

```
samples/
```

Aucune configuration particulière n'est nécessaire.

Le Benchmark analyse automatiquement tous les fichiers compatibles.

---

# Benchmark Runner

Le Runner pilote l'ensemble du processus.

Pour chaque projet :

```
ouvrir

↓

analyser

↓

reconstruire

↓

mesurer

↓

enregistrer
```

Le Runner ne réalise aucune analyse lui-même.

Il orchestre simplement les différents composants du framework.

---

# Benchmark Result

Chaque projet produit un résultat indépendant.

Exemple :

```
Hospitaliens.c2p

Objects

548

Recovered

544

Unknown

4

Properties

12418

Average confidence

0.961

Duration

0.84 s
```

Cette structure est volontairement immuable afin de faciliter les comparaisons entre versions.

---

# Benchmark Statistics

Les résultats individuels sont ensuite regroupés.

Exemple :

```
Projects

18
```

```
Objects

15234
```

```
Recovered

14998
```

```
Recovery rate

98.45 %
```

```
Average confidence

0.947
```

```
Unknown signatures

7
```

Ces statistiques permettent de suivre objectivement les progrès du projet.

---

# Benchmark Report

Le rapport constitue la sortie finale.

Plusieurs formats sont prévus.

## Console

Résumé rapide.

---

## JSON

Traitement automatique.

---

## Markdown

Documentation GitHub.

---

## HTML

Rapport interactif.

---

# Mesures réalisées

Le Benchmark calculera progressivement un grand nombre d'indicateurs.

Par exemple :

## Taille des projets

```
Minimum
```

```
Maximum
```

```
Moyenne
```

---

## Temps d'analyse

```
Projet le plus rapide
```

```
Projet le plus long
```

```
Temps moyen
```

---

## Reconstruction

```
Nombre d'objets
```

```
Objets reconstruits
```

```
Objets inconnus
```

```
Taux de reconstruction
```

---

## Discovery Engine

```
Observations
```

```
Candidates
```

```
Contraintes
```

```
Conflits
```

```
Confiance moyenne
```

---

## Knowledge Engine

```
Nouvelles signatures
```

```
Nouveaux offsets
```

```
Nouvelles règles
```

```
Connaissances enrichies
```

---

# Évolution du moteur

L'un des principaux objectifs est de conserver l'historique des Benchmarks.

Par exemple :

| Version | Tests | Projets | Reconstruction | Confiance | Temps |
|---------:|------:|---------:|---------------:|----------:|------:|
| 0.1 | 1523 | 18 | 92.4 % | 0.91 | 18.2 s |
| 0.2 | 1608 | 18 | 95.6 % | 0.94 | 17.1 s |
| 0.3 | 1724 | 18 | 97.8 % | 0.96 | 16.3 s |

Cette évolution permettra de mesurer les progrès réels du framework.

---

# Corpus de référence

Le dossier `samples/` constitue un élément essentiel du projet.

Chaque fichier Capture apporte :

- de nouvelles structures ;
- de nouveaux objets ;
- de nouvelles signatures ;
- de nouvelles propriétés.

Plus le corpus est riche, plus le moteur devient performant.

Le Benchmark garantit que chaque amélioration est validée sur des cas réels.

---

# Développement piloté par les données

Capture Recovery adopte désormais deux niveaux de validation.

## Niveau 1

Les tests unitaires garantissent la stabilité du code.

## Niveau 2

Le Benchmark garantit l'amélioration réelle du moteur.

Ces deux approches sont complémentaires.

Les tests empêchent les régressions fonctionnelles.

Le Benchmark mesure la progression des performances.

---

# Vision

À terme, le Benchmark deviendra un outil de validation continue.

Chaque évolution du framework sera évaluée automatiquement sur l'ensemble du corpus.

Les rapports permettront de répondre immédiatement à des questions telles que :

- Le moteur découvre-t-il davantage de propriétés ?
- La confiance moyenne progresse-t-elle ?
- Le nombre d'objets reconstruits augmente-t-il ?
- De nouvelles signatures ont-elles été identifiées ?
- Les performances restent-elles satisfaisantes ?

Ainsi, le développement de Capture Recovery sera guidé non seulement par la qualité du code, mais également par des mesures objectives obtenues sur des projets Capture réels.

# User Guide

Ce chapitre présente l'utilisation quotidienne de Capture Recovery.

Il décrit les commandes disponibles, le fonctionnement général du framework ainsi que l'interprétation des résultats produits.

L'objectif est de permettre à un nouvel utilisateur d'analyser un projet Capture en quelques minutes.

---

# Prérequis

Capture Recovery est développé en Python.

Versions supportées :

- Python 3.11
- Python 3.12
- Python 3.13
- versions ultérieures compatibles

Systèmes d'exploitation :

- Windows
- Linux
- macOS

---

# Installation

Cloner le dépôt :

```bash
git clone https://github.com/hennautstephan-pixel/capture.git
```

Se placer dans le dossier :

```bash
cd capture
```

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activation sous Windows :

```bash
.venv\Scripts\activate
```

Activation sous Linux/macOS :

```bash
source .venv/bin/activate
```

Installation :

```bash
pip install -e .
```

---

# Vérification de l'installation

Exécuter :

```bash
python -m pytest
```

Tous les tests doivent réussir.

Exemple :

```
====================

1523 passed

====================
```

---

# Premier projet

Le dossier `samples/` contient plusieurs projets Capture.

Exemple :

```
samples/

    Vide.c2p

    Fixture.c2p

    Theatre.c2p

    Hospitaliens.c2p
```

Ces fichiers servent à découvrir le fonctionnement du framework.

---

# Analyse d'un projet

Commande :

```bash
python capture_scan.py samples/Hospitaliens.c2p
```

Le moteur effectue automatiquement :

1. lecture du fichier ;
2. analyse des structures ;
3. découverte des propriétés ;
4. génération du rapport.

---

# Analyse de deux projets

Comparer deux versions :

```bash
python capture_diff.py \
    samples/Avant.c2p \
    samples/Apres.c2p
```

Le Diff Engine détecte automatiquement :

- les propriétés modifiées ;
- les nouveaux objets ;
- les objets supprimés ;
- les offsets concernés.

---

# Analyse complète

Le pipeline exécuté est le suivant :

```
Lecture

↓

Scan

↓

Détection

↓

Diff

↓

Discovery

↓

Validation

↓

Reconstruction

↓

Rapport
```

Chaque étape est indépendante.

---

# Lecture des résultats

Le rapport contient plusieurs catégories d'informations.

## Informations générales

```
Nom du projet

Version Capture

Taille du fichier

Durée d'analyse
```

---

## Objets

Pour chaque objet :

```
Type

Offset

Taille

Etat
```

---

## Propriétés

Pour chaque propriété :

```
Nom

Type

Valeur

Confiance

Contraintes
```

Exemple :

```
Intensity

Type

uint8

Confiance

0.98

Contraintes

Range(0..255)

Step(1)
```

---

# Contraintes

Le moteur peut identifier plusieurs contraintes.

Exemple :

```
Range

0..255
```

```
Enum

0

64

128

255
```

```
Step

5
```

```
Bitmask

0x0F
```

Ces contraintes décrivent le comportement probable de la propriété.

---

# Niveau de confiance

Chaque découverte possède une confiance.

Par exemple :

```
0.99
```

Très forte probabilité.

---

```
0.90
```

Très probable.

---

```
0.75
```

Hypothèse crédible.

---

```
0.50
```

Information encore incertaine.

---

# Conflits

Le moteur peut signaler des conflits.

Exemple :

```
Range

0..255
```

et

```
Enum

1024

2048
```

Le rapport indique alors :

```
Constraint Conflict
```

Ces conflits permettent d'identifier rapidement les hypothèses contradictoires.

---

# Export JSON

Les résultats peuvent être exportés.

Exemple :

```bash
python capture_scan.py \
    projet.c2p \
    --json rapport.json
```

Le fichier généré peut être utilisé par d'autres outils.

---

# Export HTML

À terme :

```bash
python capture_scan.py \
    projet.c2p \
    --html rapport.html
```

Le rapport HTML permettra une exploration interactive.

---

# Benchmark

Le Benchmark analyse automatiquement tous les projets du dossier `samples`.

Commande prévue :

```bash
python -m capture_recovery.benchmark samples/
```

Le rapport indiquera notamment :

```
Nombre de projets

Objets analysés

Objets reconstruits

Confiance moyenne

Temps d'exécution
```

---

# Utilisation recommandée

Pour le reverse engineering :

1. créer un projet minimal ;
2. modifier une seule propriété dans Capture ;
3. enregistrer ;
4. comparer les deux fichiers ;
5. analyser les différences.

Cette méthode permet d'identifier progressivement la signification des offsets.

---

# Interprétation

Capture Recovery ne prétend pas toujours fournir une réponse certaine.

Le framework produit des hypothèses accompagnées :

- d'un niveau de confiance ;
- de contraintes ;
- d'une justification.

Cette approche est plus adaptée au reverse engineering qu'une réponse binaire.

---

# Conseils

Pour obtenir les meilleurs résultats :

- modifier une seule propriété entre deux projets ;
- conserver les projets de référence ;
- utiliser régulièrement le dossier `samples` ;
- exécuter les tests après chaque évolution du code.

---

# Limitations actuelles

Le projet est toujours en développement.

Certaines fonctionnalités sont encore incomplètes :

- reconstruction totale des projets ;
- base de connaissances ;
- apprentissage automatique ;
- rapports HTML interactifs.

Ces fonctionnalités seront ajoutées progressivement sans modifier l'architecture actuelle.

---

# Bonnes pratiques

Avant toute modification importante :

1. lancer tous les tests ;
2. vérifier le Benchmark ;
3. documenter les nouvelles découvertes ;
4. ajouter un exemple dans `samples` si nécessaire.

Cette méthode garantit la stabilité et la reproductibilité des analyses.


# Developer Guide

Cette section s'adresse aux développeurs souhaitant contribuer au projet Capture Recovery.

Elle décrit les conventions de développement, l'architecture logicielle et les bonnes pratiques à respecter afin de conserver un framework cohérent, testable et évolutif.

---

# Philosophie de développement

Le projet repose sur cinq principes.

## 1. Une responsabilité par classe

Chaque classe ne doit réaliser qu'une seule tâche.

Exemple :

```
BinaryReader

↓

Lecture binaire uniquement
```

```
ConstraintValidator

↓

Validation uniquement
```

```
ConfidenceAggregator

↓

Calcul de confiance uniquement
```

Une classe ne doit jamais mélanger plusieurs responsabilités.

---

## 2. Dépendances à sens unique

L'architecture est organisée en couches.

```
Benchmark

        ▲

Reconstruction

        ▲

Knowledge

        ▲

Discovery

        ▲

Diff

        ▲

Binary
```

Une couche basse ne doit jamais dépendre d'une couche supérieure.

Cette règle simplifie énormément les évolutions.

---

## 3. Immutabilité

Toutes les structures représentant des données doivent être immuables.

Exemple :

```python
@dataclass(frozen=True, slots=True)
```

Cette approche apporte plusieurs avantages :

- sécurité ;
- simplicité ;
- meilleure testabilité ;
- absence d'effets de bord.

---

## 4. Tests systématiques

Toute nouvelle fonctionnalité doit être accompagnée de tests.

Aucun composant ne doit être ajouté sans validation.

---

## 5. Documentation

Chaque module doit contenir :

- un docstring ;
- des annotations de type ;
- des noms explicites ;
- une documentation utilisateur si nécessaire.

---

# Organisation des modules

Chaque module possède son propre dossier de tests.

Exemple :

```
src/

    discovery/

        enum_correlator.py
```

↓

```
tests/

    discovery/

        test_enum_correlator.py
```

Cette organisation facilite la maintenance.

---

# Ajouter un nouveau corrélateur

Les corrélateurs sont totalement indépendants.

Étapes :

Créer une nouvelle classe.

Exemple :

```
AffineCorrelator
```

Implémenter :

```
priority()
```

```
supports()
```

```
correlate()
```

Ajouter ensuite le corrélateur dans le registre.

Enfin créer les tests correspondants.

Aucune autre modification n'est nécessaire.

---

# Ajouter une nouvelle contrainte

Même principe.

Créer une nouvelle classe.

Exemple :

```
RegexConstraint
```

Ajouter ensuite :

- son corrélateur ;
- ses tests ;
- sa validation dans ConstraintValidator.

Le reste du moteur reste inchangé.

---

# Ajouter un Benchmark

Créer un nouveau calcul dans :

```
BenchmarkStatistics
```

Le résultat sera automatiquement disponible pour :

- le rapport Markdown ;
- le rapport JSON ;
- le rapport HTML.

---

# Ajouter une connaissance

Toute nouvelle connaissance doit être représentée par une structure dédiée.

Exemple :

```
KnownOffset
```

```
KnownSignature
```

```
KnownProperty
```

Éviter les dictionnaires génériques.

Les structures fortement typées facilitent les évolutions futures.

---

# Convention de nommage

Classes :

```
PascalCase
```

Modules :

```
snake_case.py
```

Fonctions :

```
snake_case()
```

Constantes :

```
UPPER_CASE
```

Variables privées :

```
_name
```

---

# Typage

Toutes les fonctions publiques doivent être annotées.

Exemple :

```python
def merge(
    self,
    candidates: list[PropertyCandidate],
) -> list[PropertyCandidate]:
```

Le typage fait partie intégrante de la documentation.

---

# Exceptions

Les exceptions doivent être utilisées uniquement pour les situations réellement exceptionnelles.

Une découverte incertaine ne doit jamais provoquer une exception.

Elle doit produire :

- une hypothèse ;
- un faible niveau de confiance ;
- éventuellement un conflit.

---

# Écriture des tests

Chaque nouveau composant doit posséder des tests couvrant :

- le fonctionnement normal ;
- les cas limites ;
- les erreurs ;
- les valeurs extrêmes ;
- les régressions identifiées.

L'objectif est de conserver une suite de tests fiable et rapide.

---

# Benchmark avant fusion

Avant d'intégrer une évolution importante :

1. lancer les tests unitaires ;
2. exécuter le Benchmark sur le dossier `samples/` ;
3. comparer les résultats avec la version précédente.

Une amélioration n'est validée que si :

- les tests restent verts ;
- le Benchmark ne montre aucune régression significative.

---

# Revue de code

Lors d'une revue, vérifier systématiquement :

- lisibilité ;
- simplicité ;
- couverture des tests ;
- documentation ;
- respect de l'architecture ;
- impact sur les performances.

---

# Évolution de l'architecture

L'architecture doit rester ouverte à l'extension.

En revanche, les modifications des interfaces publiques doivent être limitées autant que possible.

La stabilité des API facilite les développements futurs.

---

# Compatibilité

Les nouvelles fonctionnalités ne doivent pas casser :

- les tests existants ;
- les benchmarks ;
- les interfaces publiques.

Toute incompatibilité doit être clairement documentée.

---

# Vision

Capture Recovery n'est pas seulement un projet de reverse engineering.

L'objectif est de construire un framework générique capable :

- d'analyser des formats binaires complexes ;
- de produire des connaissances ;
- d'expliquer ses décisions ;
- de reconstruire des structures de haut niveau.

Toutes les contributions doivent aller dans ce sens.

Avant d'ajouter un nouveau composant, il est recommandé de se poser trois questions :

- Est-il cohérent avec l'architecture existante ?
- Peut-il être testé indépendamment ?
- Facilite-t-il les évolutions futures ?

Si la réponse est oui à ces trois questions, il s'intègre probablement correctement au framework.

# Roadmap

Capture Recovery est développé par étapes successives.

Chaque version apporte une amélioration clairement identifiée de l'architecture ou des capacités du framework.

L'objectif n'est pas d'ajouter rapidement des fonctionnalités, mais de construire progressivement un moteur de reverse engineering robuste, extensible et capable d'apprendre.

---

# État actuel

Le projet dispose aujourd'hui :

- d'une architecture modulaire stable ;
- d'un moteur de lecture binaire ;
- d'un moteur de découverte de propriétés ;
- d'un système de contraintes ;
- d'une agrégation probabiliste de la confiance ;
- d'un validateur de contraintes ;
- de plus de **1500 tests unitaires** ;
- d'un corpus de projets Capture utilisé comme référence.

L'architecture fondamentale est désormais considérée comme stable.

Les prochaines versions porteront principalement sur l'intelligence du moteur.

---

# Version 0.2

## Objectif

Mettre en place une infrastructure complète de Benchmark.

## Fonctionnalités

- BenchmarkRunner
- BenchmarkResult
- BenchmarkStatistics
- BenchmarkReport
- SampleLoader
- analyse automatique du dossier `samples`
- génération de statistiques
- rapports Markdown
- rapports JSON

## Critères de validation

- Benchmark entièrement automatisé
- comparaison de plusieurs versions
- indicateurs de performances reproductibles

---

# Version 0.3

## Objectif

Première version du Knowledge Engine.

Le moteur commencera à mémoriser automatiquement les découvertes réalisées.

## Fonctionnalités

- base de connaissances
- signatures connues
- offsets connus
- types connus
- plages observées
- historique des observations
- probabilités

## Résultat attendu

Le moteur devra commencer à améliorer ses découvertes à partir de l'expérience acquise.

---

# Version 0.4

## Objectif

Améliorer la qualité des inférences.

## Fonctionnalités

- pondération des corrélateurs
- explication des décisions
- conservation des preuves
- simplification automatique des contraintes
- gestion avancée des conflits

Cette version améliorera significativement la qualité des résultats produits.

---

# Version 0.5

## Objectif

Première reconstruction automatique des objets Capture.

Le framework devra être capable de produire une représentation cohérente de nombreux objets.

## Fonctionnalités

- Reconstruction Engine
- reconstruction des propriétés
- regroupement automatique des objets
- restauration de propriétés manquantes
- rapports détaillés

---

# Version 0.6

## Objectif

Améliorer les performances.

## Fonctionnalités

- optimisation mémoire
- optimisation CPU
- traitements parallèles
- cache des connaissances
- benchmark des performances

Le temps d'analyse devra diminuer tout en conservant la qualité des résultats.

---

# Version 0.7

## Objectif

Apprentissage automatique.

Le moteur devra commencer à apprendre sans intervention manuelle.

## Fonctionnalités

- enrichissement automatique de la base
- statistiques avancées
- apprentissage des offsets
- apprentissage des contraintes
- apprentissage des signatures

Cette étape transformera progressivement le framework en système auto-améliorant.

---

# Version 0.8

## Objectif

Documentation automatique.

Le framework devra être capable de produire automatiquement une documentation du format Capture.

## Fonctionnalités

- documentation Markdown
- documentation HTML
- cartes mémoire
- statistiques
- rapports interactifs

Chaque nouvelle découverte enrichira automatiquement la documentation.

---

# Version 0.9

## Objectif

Stabilisation.

Cette version sera consacrée à :

- optimisation
- correction des derniers défauts
- amélioration de la documentation
- nettoyage du code
- préparation de la version 1.0

---

# Version 1.0

## Objectif

Première version stable.

Le framework devra être capable :

- d'analyser un projet Capture complet ;
- de reconstruire la majorité des objets ;
- de produire une documentation détaillée ;
- d'expliquer les décisions du moteur ;
- de mesurer objectivement ses performances.

Le projet constituera alors une plateforme complète de reverse engineering du format `.c2p`.

---

# Au-delà de la version 1.0

Plusieurs pistes d'évolution sont déjà envisagées.

## Support de plusieurs versions de Capture

Le framework pourra apprendre les différences entre les versions du logiciel.

---

## Analyse d'autres formats

L'architecture actuelle est suffisamment générique pour être adaptée à d'autres formats binaires.

---

## Intelligence artificielle

Le moteur pourra exploiter des modèles probabilistes plus avancés afin de proposer plusieurs hypothèses classées par probabilité.

---

## Visualisation graphique

Une interface graphique permettra notamment :

- l'exploration de la mémoire ;
- la comparaison de projets ;
- la visualisation des structures ;
- l'inspection des objets reconstruits.

---

## Éditeur de connaissances

La base de connaissances pourra être consultée et enrichie directement depuis une interface dédiée.

---

# Mesurer les progrès

L'évolution du projet sera suivie à l'aide de plusieurs indicateurs.

## Qualité du code

- nombre de tests unitaires ;
- couverture de code ;
- stabilité des API.

---

## Qualité des analyses

- nombre d'objets reconstruits ;
- nombre de propriétés découvertes ;
- confiance moyenne ;
- conflits détectés.

---

## Performances

- temps d'analyse ;
- consommation mémoire ;
- taille de la base de connaissances.

---

## Qualité du corpus

Le dossier `samples/` constitue la référence du projet.

Chaque nouveau projet ajouté améliore la représentativité du Benchmark.

Les évolutions du framework seront systématiquement validées sur ce corpus.

---

# Vision à long terme

Capture Recovery n'a pas pour unique ambition de récupérer des fichiers corrompus.

Le projet vise à devenir une plateforme complète de reverse engineering capable de :

- comprendre automatiquement un format binaire ;
- construire progressivement une base de connaissances ;
- apprendre de nouveaux formats ;
- expliquer les décisions prises par le moteur ;
- reconstruire des structures complexes avec un niveau de confiance mesurable.

Le développement est guidé par trois principes :

- **Architecture stable**
- **Validation expérimentale**
- **Amélioration continue**

Chaque évolution doit contribuer à rendre le framework plus fiable, plus explicable et plus performant.