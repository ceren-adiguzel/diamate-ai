import sqlite3
from flask import current_app

def baglanti_al():
    # config.py içindeki DATABASE_URL değerini alır, yoksa diamate.db kullanır
    vt_yolu = current_app.config.get("DATABASE_URL", "diamate.db")
    baglanti = sqlite3.connect(vt_yolu)
    baglanti.row_factory = sqlite3.Row
    return baglanti

def veritabani_baslat(uygulama):
    """Uygulama ilk ayağa kalktığında tablo yoksa otomatik oluşturur."""
    with uygulama.app_context():
        baglanti = baglanti_al()
        imlec = baglanti.cursor()
        imlec.execute('''
            CREATE TABLE IF NOT EXISTS musteri_adaylari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                olusturulma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        baglanti.commit()
        baglanti.close()

def musteri_adayi_ekle(isim: str, telefon: str, mesaj: str):
    """Yeni bir demo/erken erişim talebini güvenli şekilde kaydeder."""
    baglanti = baglanti_al()
    imlec = baglanti.cursor()
    imlec.execute(
        "INSERT INTO musteri_adaylari (isim, telefon, mesaj) VALUES (?, ?, ?)",
        (isim, telefon, mesaj)
    )
    baglanti.commit()
    baglanti.close()

def tum_adaylari_getir() -> list:
    """Yönetim paneli için tüm kayıtları en yeniden eskiye doğru listeler."""
    baglanti = baglanti_al()
    imlec = baglanti.cursor()
    imlec.execute("SELECT * FROM musteri_adaylari ORDER BY olusturulma_tarihi DESC")
    satirlar = imlec.fetchall()
    baglanti.close()
    
    adaylar = []
    for satir in satirlar:
        adaylar.append({
            "id": satir["id"],
            "isim": satir["isim"],
            "telefon": satir["telefon"],
            "mesaj": satir["mesaj"],
            "olusturulma_tarihi": satir["olusturulma_tarihi"]
        })
    return adaylar