import time
from datetime import datetime

from veritabani.db_yoneticisi import veritabani_hazirla, db_kaydet, mod_oku
from is_mantigi.simulasyon import akilli_veri_uret, karar_motoru
from is_mantigi.donanim import baglanti_kur, veri_oku

def sistemi_baslat():
    veritabani_hazirla()
    arduino, donanim_aktif = baglanti_kur()

    if donanim_aktif:
        print("[COM3] Sınıf 1 Donanımı Hazır. Veriler devreden alınacak.")
    else:
        print("UYARI: Sınıf 1 Donanımı bulunamadı! Bağlanana kadar Sınıf 1 pas geçilecek.")
        print("Sınıf 2, 3 ve 4 için SİMÜLASYON arka planda çalışıyor...\n" + "-"*50)

    while True:
        zaman_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        aktif_mod = mod_oku() 

        for sinif_no in range(1, 5):
            veri_alindi = False

            if sinif_no == 1:
                if donanim_aktif:
                    veri_alindi, hareket, isik, sicaklik, nem = veri_oku(arduino)
            else:
                hareket, isik, sicaklik, nem = akilli_veri_uret(sinif_no, aktif_mod)
                veri_alindi = True

            if veri_alindi:
                isik_d, klima_d = karar_motoru(sinif_no, hareket, isik, sicaklik)
                db_kaydet(sinif_no, zaman_str, hareket, isik, sicaklik, nem, isik_d, klima_d)

                s_isim = "Sınıf 1 (Gerçek)" if sinif_no == 1 else f"Sınıf {sinif_no}"
                print(f"[{zaman_str}] {s_isim} [{aktif_mod[:5]}] -> H:{hareket} | {sicaklik}°C | Nem:%{nem} | Işık:{isik_d[:1]} Klima:{klima_d[:1]}")

        time.sleep(3)

if __name__ == '__main__':
    sistemi_baslat()