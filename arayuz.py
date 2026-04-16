import streamlit as st
import pandas as pd
import time
import sys
import os
from datetime import timedelta
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from veritabani.db_yoneticisi import verileri_getir, mod_oku

def ayar_yaz(yeni_mod):
    baglanti = sqlite3.connect(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'akilli_sinif.db')))
    baglanti.cursor().execute("INSERT INTO ayarlar (mod) VALUES (?)", (yeni_mod,))
    baglanti.commit()
    baglanti.close()

st.set_page_config(page_title="Akıllı Sınıf Otomasyonu", layout="wide")

# --- SİDEBAR KONTROL PANELİ ---
st.sidebar.title("⚙️ Kontrol Merkezi")

mevcut_mod = mod_oku()
gecerli_modlar = ["Doğal Akış", "Tamamen Rastgele Test"]
if mevcut_mod not in gecerli_modlar:
    mevcut_mod = "Doğal Akış"

mod_secimi = st.sidebar.radio("Simülasyon Modu Seçin:", gecerli_modlar, index=gecerli_modlar.index(mevcut_mod))

if mod_secimi != mevcut_mod:
    ayar_yaz(mod_secimi)
    st.rerun()

st.sidebar.info(f"**Aktif Veri Modeli:**\n{mod_secimi}")

# --- ANA EKRAN ---
st.title("🏫 Akıllı Sınıf Otomasyonu")
st.markdown("Sensör verilerine dayalı gerçek zamanlı kontrol ve enerji verimliliği paneli.")

sinif_secimi = st.selectbox("İncelemek İstediğiniz Sınıfı Seçin:", ["Sınıf 1 (Donanım)", "Sınıf 2", "Sınıf 3", "Sınıf 4"])
sinif_id = int(sinif_secimi.split(" ")[1])

df = verileri_getir(sinif_id)

if not df.empty:
    df['tarih_saat_obj'] = pd.to_datetime(df['tarih_saat'])
    son = df.iloc[-1]

    st.divider()
    st.subheader(f"🌐 {sinif_secimi} - Anlık Sensör Verileri")
    # "Çekilen Güç" metriği kaldırıldı, 4 kolonlu daha sade bir görünüme geçildi.
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ortam Durumu", "Dolu" if son['hareket'] == 1 else "Boş")
    c2.metric("Işık Seviyesi", f"% {son['isik_seviyesi']}")
    c3.metric("İç Sıcaklık", f"{son['sicaklik']} °C")
    c4.metric("Bağıl Nem", f"% {son['nem']}")

    st.markdown("### 🔌 Sistem (Röle) Kararları")
    r1, r2 = st.columns(2)
    r1.info(f"**💡 Aydınlatma Sistemi:** {son['isik_durumu']}")
    r2.info(f"**❄️ İklimlendirme (Klima):** {son['klima_durumu']}")

    # --- ZAMAN BAZLI ENERJİ ANALİZİ ---
    st.divider()
    st.subheader("⚡ Zaman Bazlı Enerji Verimliliği Analizi (Tahmini Modelleme)")
    st.caption("Aşağıdaki veriler, cihazların nominal çalışma güçleri (Klima: 2000W, Işık: 500W) ve rölelerin açık kalma süreleri üzerinden matematiksel olarak modellenmiştir.")
    
    zaman_araligi = st.radio("İncelemek İstediğiniz Periyodu Seçin:", 
                             ["Tüm Zamanlar", "Son 1 Hafta", "Son 1 Ay", "Son 1 Yıl"], horizontal=True)

    su_an = pd.Timestamp.now()
    if zaman_araligi == "Son 1 Hafta": df_filtreli = df[df['tarih_saat_obj'] >= (su_an - timedelta(days=7))]
    elif zaman_araligi == "Son 1 Ay": df_filtreli = df[df['tarih_saat_obj'] >= (su_an - timedelta(days=30))]
    elif zaman_araligi == "Son 1 Yıl": df_filtreli = df[df['tarih_saat_obj'] >= (su_an - timedelta(days=365))]
    else: df_filtreli = df

    # Yeni Enerji Hesaplama (Sadece rölelerin çalışma süresine göre hesaplanır)
    toplam_olcum = len(df_filtreli)
    geleneksel_tuketim = toplam_olcum * 2500.0 # Klasik sınıfta cihazlar hep açıktır (2500W)
    
    # Bizim sistem sadece AÇIK olanları hesaplar
    akilli_isik_tuketimi = len(df_filtreli[df_filtreli['isik_durumu'] == 'AÇIK']) * 500.0
    akilli_klima_tuketimi = len(df_filtreli[df_filtreli['klima_durumu'] != 'KAPALI']) * 2000.0
    akilli_tuketim = akilli_isik_tuketimi + akilli_klima_tuketimi
    
    if geleneksel_tuketim > 0:
        tasarruf_orani = ((geleneksel_tuketim - akilli_tuketim) / geleneksel_tuketim) * 100
        tasarruf_w = geleneksel_tuketim - akilli_tuketim
    else:
        tasarruf_orani, tasarruf_w = 0, 0

    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.metric(f"Verimlilik ({zaman_araligi})", f"% {tasarruf_orani:.1f}")
        st.success(f"Önlenen İsraf: **{tasarruf_w/1000:.2f} kW**")
    with col_b:
        st.bar_chart(pd.DataFrame({
            "Sistem Tipi": ["Klasik Sınıf (Sürekli Çalışan)", "Akıllı Otomasyon"],
            "Harcanan Enerji (W)": [geleneksel_tuketim, akilli_tuketim]
        }).set_index("Sistem Tipi"), color=["#3498db"])

    # Güç dalgalanması grafiği kaldırıldı, sadece sıcaklık ve nem kaldı.
    st.divider()
    st.subheader(f"📊 Ortam Değişim Grafikleri")
    g1, g2 = st.columns(2)
    with g1: st.line_chart(df_filtreli, x='tarih_saat', y='sicaklik', color='#e67e22')
    with g2: st.line_chart(df_filtreli, x='tarih_saat', y='nem', color='#3498db')

else:
    if sinif_id == 1: st.warning("⚠️ Sınıf 1 elektronik devreden veri bekliyor.")
    else: st.info("Sınıf verisi yükleniyor... Lütfen 'main_motor.py' dosyasının çalıştığından emin olun.")

time.sleep(3)
st.rerun()