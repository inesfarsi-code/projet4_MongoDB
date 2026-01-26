import os
import pandas as pd
from pymongo import MongoClient, ASCENDING


# =========================
# Configuration
# =========================
CSV_PATH = "data/healthcare_dataset.csv"

# En local (hors Docker), ça tombera sur le défaut localhost.
# Dans Docker Compose, on passera MONGO_URI=mongodb://root:rootpass@mongo:27017/admin
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

DB_NAME = "medicaldb"
COLLECTION_NAME = "admissions"


# =========================
# 1) Lecture + contrôles simples sur le CSV
# =========================
df = pd.read_csv(CSV_PATH)
print("Fichier CSV chargé")
print("Lignes initiales :", len(df))

# Déduplication (reproductible)
df = df.drop_duplicates()
print("Lignes après déduplication :", len(df))

# (Optionnel mais utile) vérifier colonnes attendues
expected_cols = [
    "Name", "Age", "Gender", "Blood Type", "Medical Condition",
    "Date of Admission", "Doctor", "Hospital", "Insurance Provider",
    "Billing Amount", "Room Number", "Admission Type", "Discharge Date",
    "Medication", "Test Results"
]
missing = [c for c in expected_cols if c not in df.columns]
if missing:
    raise ValueError(f"Colonnes manquantes dans le CSV : {missing}")


# =========================
# 2) Connexion MongoDB
# =========================
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


# =========================
# 3) Nettoyage avant import (script rejouable)
# =========================
collection.delete_many({})

