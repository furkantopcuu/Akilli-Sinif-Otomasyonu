import random

sinif_durumlari = {
    1: {"hareket_yok_sayaci": 0, "isik_durum": "KAPALI", "klima_durum": "KAPALI", "son_isik": 50.0},
    2: {"hareket_yok_sayaci": 0, "isik_durum": "KAPALI", "klima_durum": "KAPALI", "sicaklik": 22.0, "nem": 45.0, "son_isik": 50.0, "hareket_durumu": 1},
    3: {"hareket_yok_sayaci": 0, "isik_durum": "KAPALI", "klima_durum": "KAPALI", "sicaklik": 22.0, "nem": 45.0, "son_isik": 50.0, "hareket_durumu": 1},
    4: {"hareket_yok_sayaci": 0, "isik_durum": "KAPALI", "klima_durum": "KAPALI", "sicaklik": 22.0, "nem": 45.0, "son_isik": 50.0, "hareket_durumu": 1}
}

def akilli_veri_uret(sinif_no, aktif_mod):
    dr = sinif_durumlari[sinif_no]

    if aktif_mod == "Tamamen Rastgele Test":
        hareket = random.choice([0, 1])
        isik_seviyesi = round(random.uniform(10.0, 95.0), 1)
        dr["sicaklik"] = round(random.uniform(5.0, 38.0), 1)
        dr["nem"] = round(random.uniform(20.0, 80.0), 1)

    else:
        if random.random() < 0.15: 
            dr["hareket_durumu"] = 1 if dr["hareket_durumu"] == 0 else 0
        
        hareket = dr["hareket_durumu"]
        dr["son_isik"] += random.uniform(-4.0, 4.0) 
        
        if hareket == 1:
            dr["sicaklik"] += random.uniform(0.02, 0.08) 
            dr["nem"] += random.uniform(0.1, 0.3)
        else:
            dr["sicaklik"] -= random.uniform(0.05, 0.15) 
            dr["nem"] -= random.uniform(0.2, 0.5)
            
        isik_seviyesi = dr["son_isik"]

    if dr["klima_durum"] == "SOĞUTMA": dr["sicaklik"] -= random.uniform(0.2, 0.5)
    elif dr["klima_durum"] == "ISITMA": dr["sicaklik"] += random.uniform(0.2, 0.5)

    dr["sicaklik"] = max(5.0, min(38.0, dr["sicaklik"]))
    dr["nem"] = max(20.0, min(80.0, dr["nem"]))
    dr["son_isik"] = max(10.0, min(95.0, isik_seviyesi))

    return hareket, round(dr["son_isik"], 1), round(dr["sicaklik"], 1), round(dr["nem"], 1)

def karar_motoru(sinif_no, hareket, isik, sicaklik):
    dr = sinif_durumlari[sinif_no]
    
    if hareket == 1:
        dr["hareket_yok_sayaci"] = 0
        dr["isik_durum"] = "AÇIK" if isik < 50.0 else "KAPALI"
        if sicaklik > 24.0: dr["klima_durum"] = "SOĞUTMA"
        elif sicaklik < 22.0: dr["klima_durum"] = "ISITMA"
        else: dr["klima_durum"] = "KAPALI"
    else:
        dr["hareket_yok_sayaci"] += 1
        if dr["hareket_yok_sayaci"] >= 3:
            dr["isik_durum"] = "KAPALI"
            dr["klima_durum"] = "KAPALI"

    return dr["isik_durum"], dr["klima_durum"]