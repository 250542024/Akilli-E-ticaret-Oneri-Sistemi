import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

print("DB_HOST:", DB_HOST)
print("DB_NAME:", DB_NAME)
print("DB_USER:", DB_USER)
print("DB_PASSWORD:", DB_PASSWORD)
print("DB_PORT:", DB_PORT)

if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT]):
    print("❌ .env dosyası eksik veya okunamıyor!")
    exit()

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    print("✅ Bağlantı başarılı!")

    users_query = "SELECT * FROM users;"
    df_users = pd.read_sql(users_query, conn)

    print("\n👤 USERS TABLOSU:")
    print(df_users)

    products_query = "SELECT * FROM products;"
    df_products = pd.read_sql(products_query, conn)

    print("\n📦 PRODUCTS TABLOSU:")
    print(df_products)

    # 🔥 VERİ ANALİZİ (DOĞRU YER)
    print("\n📊 VERİ ANALİZİ")

    print("Ortalama fiyat:", df_products["price"].mean())

    print("\nEn pahalı ürün:")
    print(df_products.sort_values(by="price", ascending=False).head(1))

    print("\nKategori dağılımı:")
    print(df_products["category"].value_counts())

    # 🤖 ÖNERİ SİSTEMİ
    print("\n🤖 ÖNERİ SİSTEMİ")

    def butceye_gore_oner(butce):
        return df_products[df_products["price"] <= butce].sort_values(by="price", ascending=False)

    print("\n5000 TL önerileri:")
    print(butceye_gore_oner(5000))

    conn.close()

except Exception as e:
    print("❌ Hata oluştu:")
    print(e)