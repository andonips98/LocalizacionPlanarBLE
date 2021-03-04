##Script para el calculo del valor de potencia correspondiente de cada csv de fingerprint
## Filtrado de Kalman para cada baliza y posterior calculo de la media

import csv
import os
from KalmanFilter import KalmanFilter

def LimpiezaDatosCSV (ruta):
    i=0

    valores_baliza1=[]
    valores_baliza2=[]
    valores_baliza3=[]
    with open (ruta, newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            if i>0:
                valores_baliza1 = valores_baliza1 + [float(row[6])]
                valores_baliza2 = valores_baliza2 + [float(row[7])]
                valores_baliza3 = valores_baliza3 + [float(row[8])]
            
            i=i+1
      
           
    #Una vez tenemos todos los valores de potencia de todas las balizas, eliminamos los cero por desconexion de la baliza
    # y le aplicamos un filtro de Kalman y una media para tener un único valor de potencia por baliza

    Balizas=[valores_baliza1, valores_baliza2, valores_baliza3]

    RSSI_balizas=[]

    for baliza in Balizas:
        repeticiones = baliza.count(0.0)
        
        for i in range (repeticiones):
            baliza.remove(0.0)
        
        valores_filtrados = KalmanFilter(baliza)
        
        RSSI_balizas = RSSI_balizas + [sum(valores_filtrados)/len(valores_filtrados)]
    
    return RSSI_balizas



#Vamos a aplicar la función anterior a todos los csv de fingerprint

ruta_principal = 'C:\Users\Andoni Pérez\Desktop\MASTER\SEI\Bluetooth\Baliza\Mapeo\Fingerprints_Refinado'
ficheros = os.listdir('/Fingerprints_Refinado/')
fichero = 'Fingerprint_final.txt'

with open(fichero, 'w') as fichero:
        fichero.write('Los valores finales de RSSI para todas las posiciones son los siguientes: \n\n')

for ruta in ficheros:
    RSSI_balizas = LimpiezaDatosCSV(ruta_principal+ruta)
    with open('/home/pi/Desktop/Fingerprint_final.txt', 'a') as fichero:
        fichero.write(ruta)
        fichero.write(' son de ')
        fichero.write(repr(RSSI_balizas))
        fichero.write('\n\n')
        


