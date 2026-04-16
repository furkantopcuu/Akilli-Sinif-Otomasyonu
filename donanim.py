import serial
import time

PORT = 'COM3'
BAUD_RATE = 9600

def baglanti_kur():
    try:
        arduino = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
        time.sleep(2)
        return arduino, True
    except:
        return None, False

def veri_oku(arduino):
    if arduino.in_waiting > 0:
        try:
            gelen = arduino.readline().decode('utf-8').strip().split(',')
            if len(gelen) == 4:
                return True, int(gelen[0]), float(gelen[1]), float(gelen[2]), float(gelen[3])
        except: pass
    return False, 0, 0.0, 0.0, 0.0