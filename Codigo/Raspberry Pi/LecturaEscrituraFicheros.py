import csv
from datetime import datetime
from datetime import timedelta
import os.path as path
import os as os
from tramaSeguimiento import tramaSeguimiento

class LecturaEscrituraBaseDatos:
       
    def escribirBasePrincipal(self, tramasSeguimiento, nombreFichero):
        
        fichero = str(nombreFichero) + '.csv'
        
        Ubicacion = os.getcwd().split('/')
        
        if(Ubicacion[len(Ubicacion)-1] != 'BaseDatos'):
            if(path.exists(os.getcwd()+'/BaseDatos') == False ):
                os.mkdir('BaseDatos')
                
            os.chdir('BaseDatos')


        if(path.isfile(os.getcwd()+"/"+fichero)):
            with open(fichero,'a+', newline='') as csvfile:
                writer = csv.writer(csvfile,delimiter=',')
                
                for i in range(len(tramasSeguimiento)):
                    Tx = tramasSeguimiento[i].getTx()
                    TiempoComputo = tramasSeguimiento[i].getTiempoComputo()
                    row = [ tramasSeguimiento[i].getIdUser() , tramasSeguimiento[i].getMarcaTiempo(), tramasSeguimiento[i].getMarcaTiempoF(), TiempoComputo[0], TiempoComputo[1], TiempoComputo[2], Tx[0], Tx[1], Tx[2], tramasSeguimiento[i].getLugar()]
                    writer.writerow(row)
              
            csvfile.close()
        else:
            with open(fichero,'w', newline='') as csvfile:
                writer = csv.writer(csvfile,delimiter=',')
                
                header = [ 'Id Usuario', 'Marca de tiempo inicial', 'Marca de tiempo final','Tiempo de computo 1','Tiempo de computo 2','Tiempo de computo 3', 'Tx 1 (dBm)', 'Tx 2 (dBm)', 'Tx 3 (dBm)', 'Lugar']
                writer.writerow(header)
                
                for i in range(len(tramasSeguimiento)):
                    Tx = tramasSeguimiento[i].getTx()
                    TiempoComputo = tramasSeguimiento[i].getTiempoComputo()
                    row = [ tramasSeguimiento[i].getIdUser() , tramasSeguimiento[i].getMarcaTiempo(), tramasSeguimiento[i].getMarcaTiempoF(), TiempoComputo[0], TiempoComputo[1], TiempoComputo[2], Tx[0], Tx[1], Tx[2], tramasSeguimiento[i].getLugar()]
                    writer.writerow(row)
                
            csvfile.close()
      
    def traspasoBaseInicialBasePrincipal(self, nombreFichero):
        
        Lista_TramaSeguimiento = []
        fichero = str(nombreFichero) + '.csv'
        NumBaliza = []

                       
        with open(fichero, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile,delimiter = ',')
            Cabecera = True
            for row in reader:
                if (Cabecera == True):
                    Cabecera = False
                else:              
                    if (int(row[2]) != 0):
                        TramaSeguimiento_aux = tramaSeguimiento(int(row[2]),row[1])
                        
                        if (int(row[0]) == 1):
                            TramaSeguimiento_aux.setTx1(float(row[4]))
                            TramaSeguimiento_aux.setTiempoComputo1(int(row[3]))
                            NumBaliza.append(1)
                        elif (int(row[0]) == 2):
                            TramaSeguimiento_aux.setTx2(float(row[4]))
                            TramaSeguimiento_aux.setTiempoComputo2(int(row[3]))
                            NumBaliza.append(2)
                        elif (int(row[0]) == 3):
                            TramaSeguimiento_aux.setTx3(float(row[4]))
                            TramaSeguimiento_aux.setTiempoComputo3(int(row[3]))
                            NumBaliza.append(3)

                        Lista_TramaSeguimiento.append(TramaSeguimiento_aux)
                
        csvfile.close()

        TramaEscogida = []
        
        #Ordenacion temporal
        for i in range(0,len(Lista_TramaSeguimiento)):
            datetime_I = datetime.fromisoformat(Lista_TramaSeguimiento[0].getMarcaTiempo())
            
            for j in range(i+1,len(Lista_TramaSeguimiento)):
                datetime_J = datetime.fromisoformat(Lista_TramaSeguimiento[i].getMarcaTiempo())
                
                if(datetime_I > datetime_J):
                    TramaAux = Lista_TramaSeguimiento[j]
                    Lista_TramaSeguimiento[j] = Lista_TramaSeguimiento[i]
                    Lista_TramaSeguimiento[i] = TramaAux
                     
                    NumBalizaAux = NumBaliza[j]
                    NumBaliza[j] = NumBaliza[i]
                    NumBaliza[i] = NumBalizaAux                    
                    
            TramaEscogida.append(False)
        
        #Tramas generales
                    
        Lista_TramasFinales = [];
        
        for i in range(0,len(Lista_TramaSeguimiento)):
            
            Lista_TramaAux = Lista_TramaSeguimiento[i]
            
            if TramaEscogida[i] == False:
                ListaTx = [ 1 , 2 , 3 ]
                ListaTx.remove(NumBaliza[i])
                
                datetime_I = datetime.fromisoformat(Lista_TramaSeguimiento[i].getMarcaTiempo())
                ind = i + 1
                difTiempo = timedelta(seconds=0 , microseconds=0)
                
                while( ind < len(Lista_TramaSeguimiento) and difTiempo.total_seconds() < 1 and len(ListaTx) > 0):
                    datetime_J = datetime.fromisoformat(Lista_TramaSeguimiento[ind].getMarcaTiempo())
                    difTiempo = datetime_J - datetime_I
                    
                    if(Lista_TramaAux.getIdUser() == Lista_TramaSeguimiento[ind].getIdUser() and TramaEscogida[ind] == False):
                        
                        if(ListaTx.count(NumBaliza[ind]) > 0 and difTiempo.total_seconds()):
                            TramaEscogida[ind] = True
                            
                            if(NumBaliza[ind] == 1):
                                Lista_TramaAux.setTiempoComputo1(Lista_TramaSeguimiento[ind].getTiempoComputo1())
                                Lista_TramaAux.setTx1(Lista_TramaSeguimiento[ind].getTx1())
                            if(NumBaliza[ind] == 2):
                                Lista_TramaAux.setTiempoComputo2(Lista_TramaSeguimiento[ind].getTiempoComputo2())
                                Lista_TramaAux.setTx2(Lista_TramaSeguimiento[ind].getTx2())
                            if(NumBaliza[ind] == 3):
                                Lista_TramaAux.setTiempoComputo3(Lista_TramaSeguimiento[ind].getTiempoComputo3())
                                Lista_TramaAux.setTx3(Lista_TramaSeguimiento[ind].getTx3())
                                
                            ListaTx.remove(NumBaliza[ind])
                    
                    ind = ind + 1
                
                if(len(ListaTx) > 0):
                    
                    for indTx in ListaTx:
                        if(indTx == 1):
                            Lista_TramaAux.setTiempoComputo1(0)
                            Lista_TramaAux.setTx1(0)
                        if(indTx == 2):
                            Lista_TramaAux.setTiempoComputo2(0)
                            Lista_TramaAux.setTx2(0)
                        if(indTx == 3):
                            Lista_TramaAux.setTiempoComputo3(0)
                            Lista_TramaAux.setTx3(0)
                        
                marcaTF = datetime_I + difTiempo
                Lista_TramaAux.setMarcaTiempoF(marcaTF.isoformat())
                Lista_TramasFinales.append(Lista_TramaAux)
                
        print('Se borra el fichero '+fichero)
        os.remove(fichero)                
        self.escribirBasePrincipal(self, Lista_TramasFinales, "BaseDatosPrincipal")
                 

    def escribirBaseInicial(self, idBaliza, dateIsoformat, Id, tiempoComputo, RSSI, nombreFichero):
        
        fichero = str(nombreFichero) + '.csv'
        
        Ubicacion = os.getcwd().split('/')
        
        if(Ubicacion[len(Ubicacion)-1] != 'BaseDatos'):
            if(path.exists(os.getcwd()+'/BaseDatos') == False ):
                os.mkdir('BaseDatos')
                
            os.chdir('BaseDatos')
            
        if(path.isfile(os.getcwd()+"/"+fichero)):
            with open(fichero,'a+', newline='') as csvfile:
            
                writer = csv.writer(csvfile, delimiter=',')                                                                                                  
                row = [ idBaliza , dateIsoformat, Id, tiempoComputo, RSSI]
                writer.writerow(row)
                
            csvfile.close()
        else:
            with open(fichero,'w', newline='') as csvfile:
                writer = csv.writer(csvfile,delimiter=',')
            
                header = [ 'Id Baliza', 'Marca de Tiempo', 'Id Usuario', 'Tiempo Computo', 'RSSI']
                writer.writerow(header)
                row = [ idBaliza , dateIsoformat, Id, tiempoComputo, RSSI]
                writer.writerow(row)
                    
            csvfile.close()
            
        
        
        
