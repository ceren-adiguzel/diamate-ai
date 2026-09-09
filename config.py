import os
from dotenv import load_dotenv

load_dotenv()

class Ayarlar:
    # Flask ve Veritabanı 
    SECRET_KEY = os.environ.get("SECRET_KEY", "gelistirme-icin-gizli-anahtar")
    DATABASE_URL = os.environ.get("DATABASE_URL", "diamate.db")
    
    # API Anahtarları
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")
    
    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        "Rolün: Sen DiaMate platformunun resmi yapay zekâ sağlık ve tanıtım asistanısın. "
        "Firma Bilgisi: DiaMate olarak; diyabetle yaşayan bireyler için Sürekli Glukoz Takip (CGM) "
        "sensörleriyle anlık veri senkronizasyonu kuruyor, kamera tabanlı yapay zekâ analizimizle "
        "öğün ve karbonhidrat takibini otomatikleştiriyoruz. "
        "KURALLAR: "
        "1. Her zaman birinci çoğul şahıs kullan ('Biz', 'Ekibimiz', 'DiaMate olarak'). "
        "2. Kesinlikle 'Sen DiaMate olarak' gibi hatalı cümleler kurma. "
        "3. Kullanıcıya her zaman kibar, empatik, güvenilir ve profesyonel bir destek asistanı gibi yaklaş. "
        "4. Tıbbi bir teşhis koyamayacağını, tedavi öneremeyeceğini, her zaman hekime danışılması gerektiğini net şekilde belirt. "
        "5. Yanıtların kısa, net ve tamamen Türkçe olsun. "
        "6. Kullanıcıyı sitemizdeki formu doldurarak 'Erken Erişim / Demo Talep Etmeye' yönlendir."
    )
    CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "*")

class GelistirmeAyarlari(Ayarlar):
    DEBUG = True

class UretimAyarlari(Ayarlar):
    DEBUG = False

ayar_secici = {
    "gelistirme": GelistirmeAyarlari,
    "uretim": UretimAyarlari,
}