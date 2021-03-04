from LecturaEscrituraFicheros import LecturaEscrituraBaseDatos
from datetime import datetime
from datetime import timedelta
import os.path as path
import os as os
import time


Ubicacion = os.getcwd().split('/')
        
if(Ubicacion[len(Ubicacion)-1] != 'BaseDatos'):
    if(path.exists(os.getcwd()+'/BaseDatos') == False ):
        os.mkdir('BaseDatos')
        
    os.chdir('BaseDatos')


ListaFicheros = os.listdir()
ListaFicheros.sort()
datetimeActual = datetime.now()
hayFicheros = False


# Para una sola iteración, sin espera de los 15 min
for ind in range(0,len(ListaFicheros)):
    
    if (ListaFicheros[ind].__contains__('.csv') and ListaFicheros[ind].__contains__('_H_')):
        if(len(ListaFicheros[ind].split('_H_')[1].split('_')) == 2):
            hayFicheros = True
            print('Guardado datos del fichero '+ListaFicheros[ind])
            LecturaEscrituraBaseDatos.traspasoBaseInicialBasePrincipal(LecturaEscrituraBaseDatos,ListaFicheros[ind].split(".")[0])

    if(hayFicheros==False):
        print("No hay ficheros nuevos que actualizar")
        
print("¡Proceso de actualización completado!")

# Para una iteracción continuada, leyendo aquellos ficheros correspopndiente al cuarto de hora anterior
""" 
while True:

    ListaFicheros = os.listdir()
    datetimeActual = datetime.now()
    hayFicheros = False

    for ind in range(0,len(ListaFicheros)):
        
        if (ListaFicheros[ind].__contains__('.csv') and ListaFicheros[ind].__contains__('_H_')):
            if(len(ListaFicheros[ind].split('_H_')[1].split('_')) == 2):
                FechaFicheroIsoStrPrev = ListaFicheros[ind].split('_H_')[0]+'T'
                FechaFicheroIsoStrPost = ListaFicheros[ind].split('_H_')[1].split('_')[0]+':'+ListaFicheros[ind].split('_H_')[1].split('_')[1].split('.')[0]+':00'
                FechaFicheroIsoStr = FechaFicheroIsoStrPrev+FechaFicheroIsoStrPost
                datetimeFichero = datetime.fromisoformat(FechaFicheroIsoStr)
                
                difTiempo = datetimeActual - datetimeFichero
                
                if(difTiempo.total_seconds() > 15*60):
                    hayFicheros = True
                    print('Guardado datos del fichero '+ListaFicheros[ind])
                    LecturaEscrituraBaseDatos.traspasoBaseInicialBasePrincipal(LecturaEscrituraBaseDatos,ListaFicheros[ind].split(".")[0])
                    
    if(hayFicheros==False):
        print("No hay ficheros nuevos que actualizar")
    
    print("Proceso de actualización suspendido durante 15 minutos")
    time.sleep(15*60)
"""






