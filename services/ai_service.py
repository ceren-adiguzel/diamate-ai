import logging
import requests
from flask import current_app

loglayici = logging.getLogger(__name__)

class YapayZekaServisi:
    def yanit_uret(self, kullanici_mesaji: str, sohbet_gecmisi: list = None) -> str:
        saglayici = current_app.config.get("AI_PROVIDER", "gemini").lower()

        if saglayici == "openai":
            return self._openai_cagir(kullanici_mesaji, sohbet_gecmisi or [])
        elif saglayici == "groq":
            return self._groq_cagir(kullanici_mesaji, sohbet_gecmisi or [])
        else:
            return self._gemini_cagir(kullanici_mesaji, sohbet_gecmisi or [])

    def _sistem_talimati_olustur(self) -> str:
        return current_app.config.get(
            "BUSINESS_CONTEXT",
            "Sen DiaMate sağlık asistanısın."
        )

    def _gemini_cagir(self, kullanici_mesaji: str, gecmis: list) -> str:
        api_anahtari = current_app.config.get("GEMINI_API_KEY", "").strip()

        if not api_anahtari:
            loglayici.warning("GEMINI_API_KEY ayarlanmamış! Demo modu devrede.")
            return self._demo_yaniti_ver(kullanici_mesaji)

        # Kararlı v1 endpoint ve gemini-2.5-flash
        baglanti_adresi = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_anahtari}"
        
        contents = []
        sistem_mesaji = self._sistem_talimati_olustur()

        # Geçmiş boşsa sistem talimatını kullanıcı mesajıyla birleştirerek gönderiyoruz
        if not gecmis:
            contents.append({
                "role": "user",
                "parts": [{"text": f"[Sistem Talimatı: {sistem_mesaji}]\n\nKullanıcı: {kullanici_mesaji}"}]
            })
        else:
            for m in gecmis:
                rol = "model" if m.get("role") in ["assistant", "ai"] else "user"
                contents.append({
                    "role": rol,
                    "parts": [{"text": m.get("content", "")}]
                })
            contents.append({
                "role": "user",
                "parts": [{"text": kullanici_mesaji}]
            })

        gonderilecek_veri = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500
            }
        }

        try:
            sunucu_cevabi = requests.post(
                baglanti_adresi,
                json=gonderilecek_veri,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if sunucu_cevabi.status_code != 200:
                hata_json = sunucu_cevabi.json() if sunucu_cevabi.text.startswith("{") else {}
                hata_mesaji = hata_json.get("error", {}).get("message", sunucu_cevabi.text)
                print(f"\n[GEMINI API HATASI]: {hata_mesaji}\n")
                raise YapayZekaServisHatasi(f"Gemini Hatası ({sunucu_cevabi.status_code}): {hata_mesaji}")

            gelen_veri = sunucu_cevabi.json()
            uretilen_metin = gelen_veri["candidates"][0]["content"]["parts"][0]["text"]
            return uretilen_metin.strip()

        except requests.exceptions.RequestException as e:
            print(f"\n[BAGLANTI HATASI]: {e}\n")
            raise YapayZekaServisHatasi("Gemini sunucusuna bağlanılamadı.")

    def _groq_cagir(self, kullanici_mesaji: str, gecmis: list) -> str:
        api_anahtari = current_app.config.get("GROQ_API_KEY", "").strip()
        if not api_anahtari:
            return self._demo_yaniti_ver(kullanici_mesaji)
        return "Groq servisi aktif."

    def _openai_cagir(self, kullanici_mesaji: str, gecmis: list) -> str:
        return "OpenAI servisi aktif."

    def _demo_yaniti_ver(self, kullanici_mesaji: str) -> str:
        return "Sistem API anahtarı bulunamadığı için demo modunda çalışıyor. Lütfen .env dosyanızı kontrol ediniz."

class YapayZekaServisHatasi(Exception):
    pass

yapay_zeka_servisi = YapayZekaServisi()