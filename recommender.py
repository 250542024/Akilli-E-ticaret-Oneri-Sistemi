import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import joblib
import os

class ProductRecommender:
    def __init__(self):
        self.model = None
        self.product_matrix = None
        self.products = [
            {"id": 1, "name": "Kablosuz Kulaklık",    "category": "Elektronik", "fiyat": 500},
            {"id": 2, "name": "Bluetooth Hoparlör",   "category": "Elektronik", "fiyat": 300},
            {"id": 3, "name": "Akıllı Saat",          "category": "Elektronik", "fiyat": 800},
            {"id": 4, "name": "Laptop Standı",        "category": "Aksesuar",   "fiyat": 200},
            {"id": 5, "name": "Mekanik Klavye",       "category": "Aksesuar",   "fiyat": 450},
            {"id": 6, "name": "USB Hub",              "category": "Aksesuar",   "fiyat": 150},
        ]
        self._build_matrix()

    def _build_matrix(self):
        # Ürün özellik matrisi oluştur
        df = pd.DataFrame(self.products)
        df["category_code"] = pd.Categorical(df["category"]).codes
        features = df[["fiyat", "category_code"]].values
        scaler = StandardScaler()
        self.product_matrix = scaler.fit_transform(features)

    def recommend(self, user_id, threshold=0.70, top_n=5):
        # Kullanıcı ID'sine göre başlangıç ürünü seç (simülasyon)
        seed_index = user_id % len(self.products)
        seed_vector = self.product_matrix[seed_index].reshape(1, -1)

        # Kosinüs benzerliği hesapla
        scores = cosine_similarity(seed_vector, self.product_matrix)[0]

        results = []
        for i, score in enumerate(scores):
            if i == seed_index:
                continue  # Aynı ürünü önerme
            if score >= threshold:
                product = self.products[i].copy()
                product["similarity_score"] = round(float(score), 4)
                results.append(product)

        # Skora göre sırala
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_n]

# Modeli kaydet
if __name__ == "__main__":
    rec = ProductRecommender()
    joblib.dump(rec, "recommender_model.pkl")
    print("Model kaydedildi: recommender_model.pkl")
    
    # Test
    test = rec.recommend(user_id=1)
    print(f"Test onerileri: {test}")