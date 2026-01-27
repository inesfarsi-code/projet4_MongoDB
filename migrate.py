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


# =========================
# 4) Transformation (CSV -> documents MongoDB)
# =========================
documents = []
for _, row in df.iterrows():
    doc = {
        "patient": {
            "name": str(row["Name"]),
            "age": int(row["Age"]),
            "gender": str(row["Gender"]),
            "blood_type": str(row["Blood Type"]),
        },
        "medical": {
            "condition": str(row["Medical Condition"]),
            "medication": str(row["Medication"]),
            "test_results": str(row["Test Results"]),
        },
        "facility": {
            "doctor": str(row["Doctor"]),
            "hospital": str(row["Hospital"]),
            "insurance_provider": str(row["Insurance Provider"]),
            "room_number": int(row["Room Number"]),
        },
        "stay": {
            "admission_date": str(row["Date of Admission"]),
            "discharge_date": str(row["Discharge Date"]),
            "admission_type": str(row["Admission Type"]),
        },
        "billing_amount": float(row["Billing Amount"]),
    }
    documents.append(doc)


# =========================
# 5) Insertion
# =========================
result = collection.insert_many(documents)
print(f"{len(result.inserted_ids)} documents insérés dans MongoDB")


# =========================
# 6) Index (performance)
# =========================
collection.create_index([("stay.admission_date", ASCENDING)])
collection.create_index([("facility.hospital", ASCENDING)])
collection.create_index([("medical.condition", ASCENDING)])
print("Index créés avec succès")


# =========================
# 7) Vérification post-migration
# =========================
count_db = collection.count_documents({})
print("Documents en base :", count_db)

if count_db != len(df):
    raise ValueError("Incohérence entre le nombre de lignes du CSV et le nombre de documents en base")

print(" Migration terminée avec succès et vérifiée")

