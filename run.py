from app import uygulama_olustur

# Uygulama fabrikasından (factory) yapılandırılmış Flask uygulamasını alıyoruz
uygulama = uygulama_olustur()

if __name__ == "__main__":
    """
    Uygulamanın Doğrudan Çalıştırılma Kontrolü:
    Terminalden 'python run.py' komutu verildiğinde Flask geliştirme sunucusunu ayağa kaldırır.
    """
    uygulama.run(host="0.0.0.0", port=5000, debug=True)