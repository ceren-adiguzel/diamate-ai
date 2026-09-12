import json
from flask import Blueprint, request, jsonify, render_template
from services.ai_service import yapay_zeka_servisi, YapayZekaServisHatasi
from app.database import musteri_adayi_ekle, tum_adaylari_getir

api_arayuzu = Blueprint("api", __name__)
sayfa_arayuzu = Blueprint("sayfalar", __name__)

@sayfa_arayuzu.route("/")
def karsilama_sayfasi():
    return render_template("index.html")

@sayfa_arayuzu.route("/panel")
def yonetim_paneli():
    return render_template("dashboard.html")

@api_arayuzu.route("/sohbet", methods=["POST"])
def sohbet_et():
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
    veri = request.json or {}
    isim = veri.get("isim")
    mail = veri.get("mail")
    mesaj = veri.get("mesaj", "")

    if not isim or not mail:
        return jsonify({"basari": False, "hata": "İsim ve mail bilgisi zorunludur."}), 400

    musteri_adayi_ekle(isim, mail, mesaj)
    return json
    y({"basari": True, "mesaj": "Bilgileriniz başarıyla sistemimize kaydedildi."})

@api_arayuzu.route("/adaylar", methods=["GET"])
def adaylari_listele():
    adaylar = tum_adaylari_getir()
    return jsonify({"basari": True, "toplam": len(adaylar), "leadler": adaylar})