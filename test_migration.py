import unittest
import pandas as pd

# On importe les fonctions depuis notre script
from src.migrate_v3 import load_and_check_csv, transform_dataframe_to_documents


class TestMigrationPipeline(unittest.TestCase):

    def test_load_csv(self):
        """Vérifie que le CSV est bien chargé et non vide."""
        df = load_and_check_csv("data/healthcare_dataset.csv")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)

    def test_transform_documents(self):
        """Vérifie que la transformation produit des documents MongoDB valides."""
        df = load_and_check_csv("data/healthcare_dataset.csv")
        docs = transform_dataframe_to_documents(df)

        self.assertIsInstance(docs, list)
        self.assertGreater(len(docs), 0)

        sample = docs[0]

        # Vérifie la structure d'un document
        self.assertIn("patient", sample)
        self.assertIn("medical", sample)
        self.assertIn("facility", sample)
        self.assertIn("stay", sample)
        self.assertIn("billing_amount", sample)

        self.assertIn("name", sample["patient"])
        self.assertIn("condition", sample["medical"])
        self.assertIn("hospital", sample["facility"])
        self.assertIn("admission_date", sample["stay"])


if __name__ == "__main__":
    unittest.main()


