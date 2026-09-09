import os
from flask import Flask
from flask_cors import CORS
from config import ayar_secici
from app.database import veritabani_baslat

def uygulama_olustur(ayar_adi: str = None) -> Flask:
    # Flask uygulamasını ve HTML şablonlarının aranacağı templates klasörünü tanımlıyoruz
    uygulama = Flask(__name__, template_folder="templates")

    # Ortam değişkenine göre doğru konfigürasyonu seçip uygulamaya yüklüyoruz
    if ayar_adi is None:
        ayar_adi = os.environ.get("FLASK_ORTAMI", "gelistirme")
    secilen_ayar = ayar_secici.get(ayar_adi, ayar_secici["gelistirme"])
    uygulama.config.from_object(secilen_ayar)

    # CORS ayarları
    CORS(
        uygulama,
        origins=uygulama.config.get("CORS_ALLOWED_ORIGINS", "*"),
        methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    # Uygulama bağlamında veritabanı tablosunu kontrol edip yoksa oluşturuyoruz
    with uygulama.app_context():
        veritabani_baslat(uygulama)

    # Rotaları ana sisteme monte ediyoruz
    from app.routes import api_arayuzu, sayfa_arayuzu
    uygulama.register_blueprint(api_arayuzu, url_prefix="/api")
    uygulama.register_blueprint(sayfa_arayuzu)

    @uygulama.route("/saglik-durumu")
    def saglik_kontrolu():
        from flask import jsonify
        return jsonify({"durum": "aktif", "servis": "DiaMate AI API"}), 200

    return uygulama