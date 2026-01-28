import pandas as pd
from src.migrate_v3 import transform_dataframe_to_documents


def test_transform_dataframe_to_documents():
    # Jeu de données minimal simulé
    data = {
        "Name": ["Alice"],
        "Age": [30],
        "Gender": ["F"],
        "Blood Type": ["O+"],
        "Medical Condition": ["Flu"],
        "Date of Admission": ["2024-01-01"],
        "Doctor": ["Dr. Smith"],
        "Hospital": ["City Hospital"],
        "Insurance Provider": ["Aetna"],
        "Billing Amount": [1234.56],
        "Room Number": [101],
        "Admission Type": ["Emergency"],
        "Discharge Date": ["2024-01-05"],
        "Medication": ["Paracetamol"],
        "Test Results": ["Normal"]
    }

    df = pd.DataFrame(data)

    documents = transform_dataframe_to_documents(df)

    # Vérifications
    assert len(documents) == 1

    doc = documents[0]

    assert doc["patient"]["name"] == "Alice"
    assert doc["patient"]["age"] == 30
    assert doc["medical"]["condition"] == "Flu"
    assert doc["facility"]["hospital"] == "City Hospital"
    assert doc["billing_amount"] == 1234.56
