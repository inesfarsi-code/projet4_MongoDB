# Migration de données médicales vers MongoDB avec Docker

## Contexte

Ce projet s’inscrit dans le cadre d’une mission de Data Engineer chez **DataSoluTech**.

Un client fournit un dataset de données médicales au format CSV et rencontre des problèmes
de performance et de scalabilité avec ses outils actuels.  
L’objectif est de proposer une solution Big Data moderne, capable de :

- gérer un volume croissant de données,
- faciliter l’évolution du schéma,
- automatiser l’ingestion des données.

La solution retenue repose sur :

- une base **MongoDB** (NoSQL orientée documents),
- un **script Python** automatisant la migration,
- une exécution **conteneurisée avec Docker**,
- des contrôles d’intégrité avant et après import.

---

## Technologies utilisées

- Python 3  
- Pandas  
- PyMongo  
- MongoDB  
- Docker & Docker Compose  

---

## Structure du projet

```text
project4-mongo/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
├── data/
│   └── healthcare_dataset.csv
└── src/
    └── migrate.py
```
data/healthcare_dataset.csv : fichier source

src/migrate.py : script de migration automatisée

requirements.txt : dépendances Python

docker-compose.yml : orchestration des conteneurs

Dockerfile : image du conteneur “migrator”

## Modèle de données MongoDB

Les données sont stockées dans la base medicaldb, collection admissions.

Chaque ligne du CSV est transformée en un document MongoDB structuré comme suit :
```json
{
  "patient": {
    "name": "...",
    "age": 30,
    "gender": "...",
    "blood_type": "..."
  },
  "medical": {
    "condition": "...",
    "medication": "...",
    "test_results": "..."
  },
  "facility": {
    "doctor": "...",
    "hospital": "...",
    "insurance_provider": "...",
    "room_number": 123
  },
  "stay": {
    "admission_date": "...",
    "discharge_date": "...",
    "admission_type": "..."
  },
  "billing_amount": 12345.67
}
```
Ce modèle orienté document permet :

une meilleure lisibilité métier,

une évolution du schéma sans migration lourde,

des requêtes efficaces sur des sous-structures.

## Fonctionnement du script de migration

Le script migrate.py exécute les étapes suivantes :

Lecture du fichier CSV avec Pandas

Suppression des doublons

Connexion à MongoDB

Nettoyage de la collection cible (script rejouable)

Transformation de chaque ligne du CSV en document MongoDB

Insertion des documents dans la collection

Création d’index pour améliorer les performances

Vérification finale du nombre de documents en base

En fin d’exécution, le script garantit que :
Nombre de lignes CSV = Nombre de documents MongoDB
En cas d’incohérence, une erreur est levée.

## Lancement du projet
Prérequis

Docker installé

Docker Compose installé

Dans le dossier du projet, exécuter :
docker compose up --build
Déroulement

Le conteneur mongo démarre

Le conteneur migrator exécute migrate.py

Les données sont importées

Les index sont créés

Le conteneur migrator s’arrête automatiquement

MongoDB reste actif avec les données persistées dans un volume

Dans les logs, on observe par exemple :
54966 documents insérés dans MongoDB  
Index créés avec succès  
Documents en base : 54966  
Migration terminée avec succès et vérifiée 
 
Cela démontre que la migration est :
fonctionnelle,
automatisée,
reproductible,
adaptée à un contexte Big Data.

## Pourquoi MongoDB ?

MongoDB est une base de données NoSQL orientée documents.  
Elle est particulièrement adaptée aux cas suivants :

- données hétérogènes ou évolutives ;
- forte volumétrie ;
- besoin de scalabilité horizontale ;
- structures imbriquées proches du métier.

Dans ce projet, chaque ligne du CSV est transformée en un document structuré autour
d’objets métiers (`patient`, `medical`, `facility`, `stay`).  
Ce modèle est beaucoup plus naturel en NoSQL qu’en base relationnelle.

MongoDB permet :

- d’ajouter facilement de nouveaux champs sans modifier tout le schéma ;
- de requêter directement sur des sous-structures (`patient.age`, `medical.condition`, etc.) ;
- de préparer une architecture scalable pour un contexte Big Data.

---

## Pourquoi Docker ?

Docker permet de rendre l’environnement :

- reproductible ;
- portable ;
- indépendant de la machine locale.

Grâce à Docker et Docker Compose :

- MongoDB est déployé automatiquement dans un conteneur ;
- le script Python de migration s’exécute dans un autre conteneur ;
- les données sont persistées via un volume ;
- un simple `docker compose up --build` suffit pour relancer toute la chaîne.

Cela garantit que :

- n’importe quel collaborateur peut exécuter le projet sans configuration complexe ;
- la migration est entièrement automatisée ;
- la solution est prête pour un futur déploiement cloud (AWS, ECS, etc.).

Docker transforme ainsi une simple migration locale en une solution professionnelle,
portable et industrialisable.

## Sécurité et authentification

Dans un contexte réel, l’accès à la base de données ne peut pas être libre.

MongoDB permet de définir des utilisateurs avec des rôles précis :

- administrateur de la base (DBA)  
- développeur applicatif  
- lecteur (consultation uniquement)  

Dans ce projet, la connexion utilise un compte technique :

```text
mongodb://root:rootpass@mongo:27017/admin


## Tests unitaires

Le projet inclut des tests automatisés afin de valider les étapes critiques du pipeline.

Les tests vérifient notamment :

- que le fichier CSV est bien chargé ;
- que les données sont correctement transformées en documents MongoDB ;
- que la structure des documents respecte le modèle attendu.

Ces tests sont écrits avec le module `unittest` de Python.

Ils garantissent que :

- chaque fonction peut être validée indépendamment ;
- les évolutions futures du code ne cassent pas le pipeline ;
- la migration est fiable et maintenable dans le temps.

Cette approche correspond à une démarche professionnelle d’ingénierie
et permet d’industrialiser le traitement des données.
---

## Ouverture vers le cloud AWS

L’architecture mise en place avec Docker et MongoDB est conçue pour être **portable** et **scalable**.  
Elle est donc directement transposable dans un environnement cloud comme **AWS**.

L’objectif pour le client est de :

- absorber l’augmentation du volume de données,
- garantir une haute disponibilité,
- automatiser les sauvegardes,
- réduire la charge de maintenance des serveurs.

Le cloud répond à ces besoins en proposant des services managés, élastiques et sécurisés.

---

## Services AWS adaptés au projet

### Stockage des fichiers – Amazon S3

Amazon S3 est un service de stockage d’objets hautement durable et peu coûteux.

Dans ce projet, S3 pourrait être utilisé pour :

- stocker le fichier `healthcare_dataset.csv`,
- conserver les exports de données,
- archiver les historiques de migration.

Avantages :

- disponibilité très élevée,
- stockage quasi illimité,
- facturation à l’usage,
- intégration native avec les autres services AWS.

---

### Base de données – Amazon DocumentDB (compatible MongoDB)

AWS propose **Amazon DocumentDB**, un service managé compatible avec MongoDB.

Il permet de :

- conserver le modèle orienté documents,
- bénéficier d’une haute disponibilité,
- automatiser les sauvegardes,
- éviter la gestion manuelle des serveurs.

Dans un contexte de production, la base `medicaldb` pourrait être hébergée sur DocumentDB, tout en conservant le même schéma de données que celui utilisé en local.

---

### Exécution du script – Amazon ECS

Le script de migration est déjà conteneurisé avec Docker.  
Cela permet une intégration directe dans **Amazon ECS (Elastic Container Service)**.

Principe :

1. Le fichier CSV est stocké dans S3  
2. Un conteneur “migrator” est lancé via ECS  
3. Le conteneur lit le CSV depuis S3  
4. Les données sont insérées dans DocumentDB  
5. Le conteneur s’arrête automatiquement  

Architecture logique :

Amazon S3 (CSV)
│
▼
Conteneur migrator (ECS)
│
▼
Amazon DocumentDB (MongoDB)

Cette approche permet :

- des migrations reproductibles,
- une exécution à la demande,
- une montée en charge automatique,
- une intégration simple dans une chaîne CI/CD.

---

## Bénéfices pour le client

- Scalabilité horizontale  
- Haute disponibilité  
- Sauvegardes automatiques  
- Réduction des coûts d’exploitation  
- Architecture prête pour le Big Data  

Le projet local constitue ainsi un **prototype fonctionnel** prêt à être industrialisé sur AWS.

