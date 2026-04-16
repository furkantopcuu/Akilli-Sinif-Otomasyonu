import sqlite3
import pandas as pd
import os

DB_YOLU = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'akilli_sinif.db'))

def veritabani_hazirla():
    baglanti = sqlite3.connect(DB_YOLU)
    imlec = baglanti.cursor()
    
    for i in range(1, 5):
        imlec.execute(f'''
            CREATE TABLE IF NOT EXISTS sinif_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih_saat TEXT, hareket INTEGER, isik_seviyesi REAL,
                sicaklik REAL, nem REAL,
                isik_durumu TEXT, klima_durumu TEXT
            )
        ''')
        
    imlec.execute('CREATE TABLE IF NOT EXISTS ayarlar (id INTEGER PRIMARY KEY, mod TEXT)')
    imlec.execute('SELECT COUNT(*) FROM ayarlar')
    if imlec.fetchone()[0] == 0:
        imlec.execute('INSERT INTO ayarlar (mod) VALUES ("Doğal Akış")')
        
    baglanti.commit()
    baglanti.close()

def db_kaydet(sinif_no, zaman, hareket, isik_sev, sicaklik, nem, isik_d, klima_d):
    baglanti = sqlite3.connect(DB_YOLU)
    baglanti.cursor().execute(
        f"INSERT INTO sinif_{sinif_no} (tarih_saat, hareket, isik_seviyesi, sicaklik, nem, isik_durumu, klima_durumu) VALUES (?, ?, ?, ?, ?, ?, ?)", 
        (zaman, hareket, isik_sev, sicaklik, nem, isik_d, klima_d)
    )
    baglanti.commit()
    baglanti.close()

def verileri_getir(sinif_no):
    try:
        baglanti = sqlite3.connect(DB_YOLU)
        df = pd.read_sql_query(f"SELECT * FROM sinif_{sinif_no}", baglanti)
        baglanti.close()
        return df
    except:
        return pd.DataFrame()

def mod_oku():
    try:
        baglanti = sqlite3.connect(DB_YOLU)
        mod = baglanti.cursor().execute("SELECT mod FROM ayarlar ORDER BY id DESC LIMIT 1").fetchone()[0]
        baglanti.close()
        return mod
    except: return "Doğal Akış"