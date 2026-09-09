from flask import Blueprint, request, jsonify, render_template
from services.ai_service import yapay_zeka_servisi, YapayZekaServisHatasi
from app.database import musteri_adayi_ekle, tum_adaylari_getir

# Rotaları gruplandırmak için Blueprint nesneleri oluşturuyoruz
api_arayuzu = Blueprint("api", __name__)
sayfa_arayuzu = Blueprint("sayfalar", __name__)


# ─── SAYFALAR (Arayüzler) ─────────────────────────────

@sayfa_arayuzu.route("/")
def karsilama_sayfasi():
    """Kullanıcıya sunulan ana karşılama ve AI sohbet sayfası."""
    return render_template("index.html")

@sayfa_arayuzu.route("/panel")
def yonetim_paneli():
    """Erken erişim ve demo taleplerinin listelendiği yönetim paneli."""
    return render_template("dashboard.html")


# ─── API UÇ NOKTALARI (Endpoints) ──────────────────────

@api_arayuzu.route("/sohbet", methods=["POST"])
def sohbet_et():
    """Ön yüzden gelen soruyu alır, AI servisine iletir ve cevabı döndürür."""
    veri = request.json or {}
    mesaj = veri.get("mesaj")
    gecmis = veri.get("gecmis", [])

    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj alanı boş bırakılamaz."}), 400

    try:
        yanit = yapay_zeka_servisi.yanit_uret(mesaj, gecmis)
        return jsonify({"basari": True, "cevap": yanit})
    except YapayZekaServisHatasi as e:
        return jsonify({"basari": False, "hata": str(e)}), 503

@api_arayuzu.route("/adaylar", methods=["POST"])
def aday_kaydet():
    """İletişim/demo formundan gelen bilgileri veritabanına kaydeder."""
    veri = request.json or {}
    isim = veri.get("isim")
    telefon = veri.get("telefon")
    mesaj = veri.get("mesaj", "")

    if not isim or not telefon:
        return jsonify({"basari": False, "hata": "İsim ve telefon bilgisi zorunludur."}), 400

    musteri_adayi_ekle(isim, telefon, mesaj)
    return jsonify({"basari": True, "mesaj": "Bilgileriniz başarıyla sistemimize kaydedildi."})

@api_arayuzu.route("/adaylar", methods=["GET"])
def adaylari_listele():
    """Yönetim paneli için tüm adayları JSON olarak döndürür."""
    adaylar = tum_adaylari_getir()
    return jsonify({"basari": True, "toplam": len(adaylar), "adaylar": adaylar})