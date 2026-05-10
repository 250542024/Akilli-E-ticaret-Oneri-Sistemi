from flask import Flask, jsonify, request
import logging
import joblib
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Loglama
logging.basicConfig(filename='api_logs.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# ── Model Yükleme ──
recommender = None

def load_model():
    global recommender
    try:
        if os.path.exists("recommender_model.pkl"):
            import recommender as rec_module
            import sys
            sys.modules['__main__'].ProductRecommender = rec_module.ProductRecommender
            recommender = joblib.load("recommender_model.pkl")
            app.logger.info("Model basariyla yuklendi.")
            print("✅ Model yuklendi!")
        else:
            app.logger.warning("Model dosyasi bulunamadi, fallback aktif.")
            print("⚠️  Model bulunamadi, fallback kullanilacak.")
    except Exception as e:
        app.logger.error(f"Model yukleme hatasi: {e}")
        print(f"❌ Model hatasi: {e}")

load_model()

# ── Fallback Onerileri ──
FALLBACK = [
    {"id": 1, "name": "Kablosuz Kulaklık",  "similarity_score": 0.95},
    {"id": 2, "name": "Bluetooth Hoparlör", "similarity_score": 0.82},
    {"id": 4, "name": "Laptop Standı",      "similarity_score": 0.88},
]

# ── Endpointler ──

@app.route('/')
def home():
    model_durumu = "aktif" if recommender else "fallback"
    return jsonify({
        "mesaj": "Flask Oneri API'sine Hos Geldiniz!",
        "model_durumu": model_durumu
    })

@app.route('/api/v1/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    threshold = float(request.args.get('threshold', 0.70))
    top_n     = int(request.args.get('top_n', 5))

    if recommender:
        try:
            results = recommender.recommend(user_id, threshold=threshold, top_n=top_n)
            source  = "scikit-learn"
        except Exception as e:
            app.logger.error(f"Model tahmin hatasi: {e}")
            results = FALLBACK
            source  = "fallback"
    else:
        results = FALLBACK
        source  = "fallback"

    app.logger.info(f"Kullanici {user_id} icin {len(results)} oneri donduruldu ({source}).")

    return jsonify({
        "user_id":        user_id,
        "source":         source,
        "threshold":      threshold,
        "results_count":  len(results),
        "recommendations": results
    })

# ── Hata Yönetimi ──

@app.errorhandler(404)
def not_found(error):
    return jsonify({"hata": "Kaynak bulunamadi"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"hata": "Sunucu hatasi"}), 500

if __name__ == "__main__":
    print("FLASK BASLADI")
    print("Sunucu: http://127.0.0.1:8000")
    app.run(host="127.0.0.1", port=8000, debug=False, use_reloader=False)