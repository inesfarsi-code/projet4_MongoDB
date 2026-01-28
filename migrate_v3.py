import os
import pandas as pd
from pymongo import MongoClient, ASCENDING


# =========================
# Configuration globale
# =========================
CSV_PATH = "data/healthcare_dataset.csv"

# En local : mongodb://localhost:27017/
# En Docker : mongodb://root:rootpass@mongo:27017/admin
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

DB_NAME = "medicaldb"
COLLECTION_NAME = "admissions"


# =========================
# 1) Extraction & contrôle du CSV
# =========================
def load_and_check_csv(csv_path: str) -> pd.DataFrame:
    """
    Charge le fichier CSV dans un DataFrame Pandas
    et vérifie la présence des colonnes attendues.
    """
    print("Chargement du fichier CSV")
    df = pd.read_csv(csv_path)
    print("Lignes initiales :", len(df))

    # Suppression des doublons (script rejouable)
    df = df.drop_duplicates()
    print("Lignes après déduplication :", len(df))

    expected_cols = [
        "Name", "Age", "Gender", "Blood Type", "Medical Condition",
        "Date of Admission", "Doctor", "Hospital", "Insurance Provider",
        "Billing Amount", "Room Number", "Admission Type", "Discharge Date",
        "Medication", "Test Results"
    ]

    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes dans le CSV : {missing}")

    return df


# =========================
# 2) Connexion MongoDB
# =========================
def connect_to_mongo(uri: str, db_name: str, collection_name: str):
    """
    Établit la connexion à MongoDB et retourne la collection cible.
    """
    print("Connexion à MongoDB")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # vérifie que Mongo répond

    db = client[db_name]
    collection = db[collection_name]
    return collection



# =========================
# 3) Transformation des données
# =========================
def transform_dataframe_to_documents(df: pd.DataFrame) -> list:
    """
    Transforme chaque ligne du DataFrame en document MongoDB structuré.
    """
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

    return documents


# =========================
# 4) Chargement dans MongoDB
# =========================
def load_documents(collection, documents: list):
    """
    Vide la collection puis insère les documents.
    """
    print("Nettoyage de la collection")
    collection.delete_many({})

    print("Insertion des documents")
    result = collection.insert_many(documents)
    print(f"{len(result.inserted_ids)} documents insérés dans MongoDB")


# =========================
# 5) Index & vérification
# =========================
def create_indexes(collection):
    """
    Crée des index pour améliorer les performances.
    """
    collection.create_index([("stay.admission_date", ASCENDING)])
    collection.create_index([("facility.hospital", ASCENDING)])
    collection.create_index([("medical.condition", ASCENDING)])
    print("Index créés avec succès")


def verify_migration(collection, expected_count: int):
    """
    Vérifie que le nombre de documents en base correspond
    au nombre de lignes du CSV après déduplication.
    """
    count_db = collection.count_documents({})
    print("Documents en base :", count_db)

    if count_db != expected_count:
        raise ValueError("Incohérence entre le CSV et MongoDB")

    print("Migration terminée avec succès et vérifiée")


# =========================
# Point d’entrée principal
# =========================
def main():
    df = load_and_check_csv(CSV_PATH)
    collection = connect_to_mongo(MONGO_URI, DB_NAME, COLLECTION_NAME)
    documents = transform_dataframe_to_documents(df)
    load_documents(collection, documents)
    create_indexes(collection)
    verify_migration(collection, len(df))


if __name__ == "__main__":
    main()
