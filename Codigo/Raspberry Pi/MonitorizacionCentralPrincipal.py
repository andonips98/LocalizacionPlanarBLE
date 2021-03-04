from bluepy import btle
import struct
from concurrent import futures

from LecturaEscrituraFicheros import LecturaEscrituraBaseDatos
from datetime import datetime
from datetime import timedelta
import os.path as path
import os as os
import time

global addr_modulos
global delegates_modulos
global perifericos_modulos

addr_modulos = ['e7:90:aa:26:68:ad','e2:c3:7c:bb:72:76','d5:92:12:3f:7a:5c']


class MyDelegate(btle.DefaultDelegate):
    
    def __init__(self,params):
        btle.DefaultDelegate.__init__(self)
    
                
def loop_modulo(modulo,IdBaliza):
    
    Characteristics = modulo.getCharacteristics()
    RSSICharacteristic = Characteristics[3]
    SincronismoCharacteristic = Characteristics[4]
    TiempoComputoCharacteristic = Characteristics[5]
    IdCharacteristic = Characteristics[6]
    inicio = True
    Periferico_conectado = False
    marcaSincronismo = 0
    
    while True:
        try:           
            
            RSSI = struct.unpack("f",RSSICharacteristic.read())[0]
            marcaSincronismo  = struct.unpack("l",SincronismoCharacteristic.read())[0]
            tiempoComputo = struct.unpack("l",TiempoComputoCharacteristic.read())[0]
            IDPeriferico = struct.unpack("i",IdCharacteristic.read())[0]
            
            # Para la monitorización en pantalla, se recomienda desactivar el guardado de base para obtener mejores tiempos de lectura
            #if(RSSI != 0):
                #print("Datos RSSI del modulo nº"+str(IdBaliza+1)+": "+str(RSSI))
                #print("Marca de sincronismo del modulo nº"+str(IdBaliza+1)+": "+ str(marcaSincronismo))
                #print("Tiempo de computo del modulo nº"+str(IdBaliza+1)+": "+ str(tiempoComputo))
                #print("Id del modulo nº"+str(IdBaliza+1)+": "+ str(IDPeriferico))           
            
            if(inicio == True):
                marcaSincronismoPrev = marcaSincronismo-1
                inicio = False
            
            d = datetime.now()
            if(marcaSincronismo != marcaSincronismoPrev and RSSI < 0 and IDPeriferico != 0):
                
                if(Periferico_conectado==False):
                    print("¡Hay periferico conectado en la baliza "+str(IdBaliza+1)+" !")
                    Periferico_conectado = True
                    
                    
                marcaSincronismoPrev = marcaSincronismo
                
                if(d.minute < 15):
                    difTiempo = timedelta(minutes = 0)
                elif (d.minute < 30):
                    difTiempo = timedelta(minutes = 15)
                elif (d.minute < 45):
                    difTiempo = timedelta(minutes = 30)
                else:
                    difTiempo = timedelta(minutes = 45)
                
                e = d - timedelta(minutes = d.minute)
                e = e + difTiempo                    
                print(d.isoformat()+' Baliza: '+str(IdBaliza+1))
                nombreFicheroV = e.isoformat().split('.')[0].split('T')
                nombreFicheroHV = nombreFicheroV[1].split(':')
                nombreFicheroH = nombreFicheroHV[0]+'_'+nombreFicheroHV[1]
                nombreFichero = nombreFicheroV[0]+'_H_'+nombreFicheroH
                 
                LecturaEscrituraBaseDatos.escribirBaseInicial(LecturaEscrituraBaseDatos, IdBaliza+1, str(d.isoformat()), IDPeriferico, tiempoComputo, RSSI, nombreFichero)
            else:
                
                if(Periferico_conectado==True and marcaSincronismo == marcaSincronismoPrev):
                    print("Periferico desconectado de la baliza "+str(IdBaliza+1))
                    Periferico_conectado = False
                              
            continue
                
        except:
            try:
                modulo.disconnect()
            except:
                pass
            
            print("Reconectando dispositivo: "+modulo.addr+" . Dispositivo Nº"+str(ind+1))
            reestablecer_conexion(modulo,modulo.addr,ind)
            

delegates_modulos = []
perifericos_modulos = []
[delegates_modulos.append(0) for i in range(len(addr_modulos))]
[perifericos_modulos.append(0) for i in range(len(addr_modulos))]
            
            
def reestablecer_conexion(modulo,addr,ind):
    while True:
        try:
            print("Intentando reconectar con "+modulo.addr)
            modulo.connect(addr)
            print("Reconectado con modulo nº"+str(ind+1)+" Direccion: "+modulo.addr)
            return
        except:
            continue
        
def establecer_conexion(addr):
    global addr_modulos
    global delegates_modulos
    global perifericos_modulos
    
    while True:
        try:
            for i in range(len(addr_modulos)):
                if addr_modulos[i] == addr:
                    print("Intentando conectar con el modulo nº "+str(i+1)+". Direccion: "+addr)
                    p = btle.Peripheral()
                    p.connect(addr)
                    perifericos_modulos[i] = p
                    p_delegate = MyDelegate(addr)
                    delegates_modulos[i] = p_delegate
                    p.withDelegate(p_delegate)
                    print("Conectado dispositivo Nº "+str(i+1)+" . Direccion: "+addr)
                    loop_modulo(p,i)
        except:
            print("Fallo en conectar con dispositivo de direccion: "+addr)
            continue


ex = futures.ProcessPoolExecutor(max_workers = os.cpu_count())
results = ex.map(establecer_conexion,addr_modulos)
            