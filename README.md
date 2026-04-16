# 🏫 Akıllı Sınıf Otomasyon Sistemi

Bu proje, sınıf ortamlarında enerji verimliliğini artırmak için geliştirilmiş, sensör tabanlı bir otomasyon ve analiz panelidir. Katmanlı mimari (Layered Architecture) kullanılarak geliştirilmiştir.

## 🚀 Özellikler
* **Gerçek Zamanlı Simülasyon:** "Doğal Akış" ve "Tamamen Rastgele Test" modları.
* **Akıllı Karar Mekanizması:** Hareket ve ışığa göre otomatik röle (Işık/Klima) kontrolü.
* **Enerji Tasarrufu Analizi:** Zaman bazlı kW tasarrufu modellemesi.
* **Donanım Desteği:** Arduino entegrasyonu (Sınıf 1 için).

## 🏗️ Proje Yapısı
* **Veritabanı:** SQLite ile her sınıf için ayrı veri takibi.
* **İş Mantığı:** Sensör verisi üretme ve kontrol algoritmaları.
* **Sunum:** Streamlit ile interaktif web arayüzü.

## 🛠️ Kurulum
1. `pip install -r requirements.txt` komutuyla kütüphaneleri kurun.
2. `python main_motor.py` ile motoru başlatın.
3. `python -m streamlit run sunum/arayuz.py` ile paneli açın.
