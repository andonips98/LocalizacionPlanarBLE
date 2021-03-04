# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 13:08:02 2021

@author: Andoni
"""
import csv
from scipy.spatial import distance
import math
from KalmanFilter import KalmanFilter
from mapeo import dibujar_trayectoria

def interpolacion(valores):
      i=0
      inicio=''
      interpolando=False
      valores_interpolados=[]            
      for valor in valores:
            
            if valor==0 and inicio=='':
                  inicio = i
                  interpolando = True
            elif (interpolando==False):
                  valores_interpolados = valores_interpolados + [valor]
                  
            if valor!=0 and inicio!='':
                  aumento=(abs(valores[inicio-1])-abs(valor))/(i-inicio+1)
                  for j in range(i-inicio):
                        valores_interpolados = valores_interpolados + [valores_interpolados[len(valores_interpolados)-1]+aumento]
                  valores_interpolados = valores_interpolados + [valor]
                  interpolando = False
                  inicio=''
            i=i+1      
                        
      
      return valores_interpolados
      
      
def calculo_sala(diccionario_fingerprints,valor_baliza1,valor_baliza2,valor_baliza3,sala_anterior):
      
      
      ponderacion_Salon2 = [misma_sala, sala_1, salas_2, salas_3, salas_2, salas_3, salas_2, salas_3, sala_1, salas_3, salas_3, salas_3, salas_2, salas_3, salas_3, salas_3]
      ponderacion_Salon4 = [sala_1, misma_sala, salas_3, salas_2, sala_1, salas_2, sala_1, salas_3, salas_2, salas_3, salas_3, salas_3, salas_3, salas_2, salas_3, salas_3]
      ponderacion_Pasillo2 = [salas_2, salas_3, misma_sala, salas_3, salas_3, salas_3, salas_2, sala_1, sala_1, salas_3, salas_2, sala_1, salas_3, salas_2, sala_1, sala_1]
      ponderacion_Cuarto3_2 = [salas_3, salas_2, salas_3, misma_sala, sala_1, salas_3,salas_3,salas_3,salas_3,salas_3,salas_3,salas_3,salas_3,salas_3,salas_3,salas_3]
      ponderacion_Cuarto3_1 = [salas_2, sala_1, salas_3, sala_1, misma_sala, salas_3, salas_2, salas_3, salas_3, salas_3, salas_3, salas_3, salas_2, salas_3, salas_3, salas_3]
      ponderacion_Cuarto2 = [salas_3, salas_2, salas_3, salas_3, salas_3, misma_sala, sala_1, salas_3, salas_2, salas_3, salas_3,salas_3,salas_3,salas_3,salas_3,salas_3]
      ponderacion_Salon3 = [salas_2, sala_1, salas_2, salas_3, salas_2,sala_1 ,misma_sala,salas_3, sala_1, salas_3, salas_3, salas_3, salas_2, salas_3, salas_3, salas_3]
      ponderacion_Bano = [salas_3, salas_3, sala_1, salas_3, salas_3,salas_3,salas_3, misma_sala, salas_2, salas_3,salas_3,salas_2,salas_3,salas_2,salas_2,sala_1]
      ponderacion_Salon1 = [sala_1,salas_2,sala_1,salas_3,salas_2, salas_2, sala_1, salas_2, misma_sala, salas_3, salas_3,salas_2,salas_2,salas_3, salas_2,salas_2]
      ponderacion_Cuarto1_1 = [salas_3,salas_3,salas_3,salas_3,salas_3,salas_3,salas_3,salas_3,salas_3,misma_sala,salas_3,salas_3,salas_3,sala_1, salas_3, salas_2]
      ponderacion_Cocina2 = [salas_3,salas_3,salas_2,salas_3,salas_3,salas_3,salas_3,salas_3,salas_3,salas_3,misma_sala,salas_2,salas_3,salas_3,sala_1,salas_3]
      ponderacion_Entrada = [salas_3,salas_3,sala_1,salas_3,salas_3,salas_3,salas_3,salas_2,salas_2,salas_3,salas_2,misma_sala,salas_3,salas_3, sala_1, salas_2]
      ponderacion_Balcon = [salas_2,sala_1, salas_3,salas_3,salas_2, salas_3,salas_2,salas_3,salas_3,salas_3,salas_3,salas_3,misma_sala,salas_3,salas_3,salas_3]
      ponderacion_Cuarto1_2 = [salas_3,salas_3,salas_2,salas_3,salas_3,salas_3,salas_3,salas_2,salas_2,sala_1,salas_3,salas_3,salas_3,misma_sala, salas_3,sala_1]
      ponderacion_Cocina1 = [salas_3,salas_3, sala_1,salas_3,salas_3,salas_3,salas_3,salas_2,salas_2,salas_3,sala_1,sala_1,salas_3,salas_3,misma_sala,salas_2]
      ponderacion_Pasillo1 = [salas_3, salas_3, sala_1,salas_3,salas_3, salas_3, salas_3,sala_1,salas_2,salas_2,salas_3,salas_2,salas_3,sala_1,salas_2,misma_sala]
      ponderacion_Primera = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
      
      
      if sala_anterior == 'Primera vez':
            ponderacion = ponderacion_Primera
      elif sala_anterior == 'Salon_2':
            ponderacion = ponderacion_Salon2
      elif sala_anterior == 'Salon_4':
            ponderacion = ponderacion_Salon4
      elif sala_anterior == 'Pasillo_2':
            ponderacion = ponderacion_Pasillo2
      elif sala_anterior == 'Cuarto3_2':
            ponderacion = ponderacion_Cuarto3_2
      elif sala_anterior == 'Cuarto3_1':
            ponderacion = ponderacion_Cuarto3_1
      elif sala_anterior == 'Cuarto2':
            ponderacion = ponderacion_Cuarto2
      elif sala_anterior == 'Salon_3':
            ponderacion = ponderacion_Salon3
      elif sala_anterior == 'Baño':
            ponderacion = ponderacion_Bano
      elif sala_anterior == 'Salon_1':
            ponderacion = ponderacion_Salon1
      elif sala_anterior == 'Cuarto1_1':
            ponderacion = ponderacion_Cuarto1_1
      elif sala_anterior == 'Cocina_2':
            ponderacion = ponderacion_Cocina2
      elif sala_anterior == 'Entrada':
            ponderacion = ponderacion_Entrada
      elif sala_anterior == 'Balcon':
            ponderacion = ponderacion_Balcon
      elif sala_anterior == 'Cuarto1_2':
            ponderacion = ponderacion_Cuarto1_2
      elif sala_anterior == 'Cocina_1':
            ponderacion = ponderacion_Cocina1
      elif sala_anterior == 'Pasillo_1':
            ponderacion = ponderacion_Pasillo1
            
            
            
      distancia = []
      valores_balizas = [valor_baliza1, valor_baliza2, valor_baliza3]
      salas = diccionario_fingerprints.keys()
      distancia_anterior = ponderacion[0]*distance.euclidean(valores_balizas,[diccionario_fingerprints['Salon_2'][0],diccionario_fingerprints['Salon_2'][1],diccionario_fingerprints['Salon_2'][2]])
      localizacion = 'Salon_2'
      i=0
      for sala in salas:
            
            distancia_nueva = ponderacion[i]*distance.euclidean(valores_balizas,[diccionario_fingerprints[sala][0],diccionario_fingerprints[sala][1],diccionario_fingerprints[sala][2]])
            distancia = distancia + [distancia_nueva]
            if distancia_nueva<distancia_anterior:
                  distancia_anterior = distancia_nueva
                  localizacion = sala
            i=i+1            
      return localizacion,distancia
      


##Vectores para la ponderación de las distancias
      
misma_sala = 0.75

sala_1 = 1.25

salas_2 = 2

salas_3 = 100

#diccionario antiguo
#diccionario_fingerprints={'Salon_2': [-62.769, -64.268, -66.406], 'Salon_4': [-70.452, -68.882, -52.686], 'Pasillo_2': [-64.864, -55.216, -70.082], 'Cuarto3_2': [-73.864, -73.563, -67.309], 'Cuarto3_1': [-74.582, -74.783, -60.7], 'Cuarto2': [-69, -68.435, -58.023],'Salon_3':[-69.443, -59.673, -62.164],'Baño':[-74.808, -54.378, -74.613],'Salon_1':[-68.295, -59.782, -66.27],'Cuarto1_1':[-70.453, -59.315, -72.007],'Cocina_2':[-54.76, -74.797, -73.47],'Entrada':[-63.376, -62.211, -70.994],'Balcon':[-74.467, -66.401, -69.992],'Cuarto1_2':[-74.461, -59.331, -71.16],'Cocina_1':[-58.542, -72.914, -72.451],'Pasillo_1':[-72.086, -50.351, -71.077]}

diccionario_fingerprints={'Salon_2': [-63.674, -64.682, -65.799], 'Salon_4': [-70.414, -69.014, -52.568], 'Pasillo_2': [-65.208, -54.941, -69.041], 'Cuarto3_2': [-73.181, -73.652, -67.57], 'Cuarto3_1': [-74.447, -74.591, -56.8], 'Cuarto2': [-68.51, -68.811, -57.949],'Salon_3':[-67.592, -59.556, -64.768],'Baño':[-75.628, -53.597, -75.195],'Salon_1':[-66.276, -58.653, -67.609],'Cuarto1_1':[-73.67, -59.568, -72.276],'Cocina_2':[-54.037, -74.919, -72.307],'Entrada':[-58.157, -62.653, -71.34],'Balcon':[-75.063, -63.294, -70.603],'Cuarto1_2':[-74.747, -59.56, -70.93],'Cocina_1':[-59.491, -72.961, -72.072],'Pasillo_1':[-71.813, -49.81, -70.401]}

valores_baliza1=[]
valores_baliza2=[]
valores_baliza3=[]

i=0
with open ('Trayectoria_10_02_Salon_Cocina.csv', newline='') as File:
        reader = csv.reader(File)
        for row in reader:
              if i>0:

                    valores_baliza1 = valores_baliza1 + [float(row[6])]
                    valores_baliza2 = valores_baliza2 + [float(row[7])]
                    valores_baliza3 = valores_baliza3 + [float(row[8])]
                    
#                    
              i=i+1
              
              
              
#Interpolamos los valores de potencia por breves desconexiones
              

valores_baliza1_inter=interpolacion(valores_baliza1)
valores_baliza2_inter=interpolacion(valores_baliza2)
valores_baliza3_inter=interpolacion(valores_baliza3)

#Aplicamos Kalman a los valores de las balizas
numero_tramas = 2

valores_baliza1_inter=valores_baliza1_inter[:math.floor(len(valores_baliza1_inter)/numero_tramas)*numero_tramas]
j=0
for i in range (int(len(valores_baliza1_inter)/numero_tramas)):
      valores_baliza1_inter[j:j+numero_tramas] = KalmanFilter(valores_baliza1_inter[j:j+numero_tramas])
      j=j+numero_tramas
      
valores_baliza2_inter=valores_baliza2_inter[:math.floor(len(valores_baliza2_inter)/numero_tramas)*numero_tramas]
j=0
for i in range (int(len(valores_baliza2_inter)/numero_tramas)):
      valores_baliza2_inter[j:j+numero_tramas] = KalmanFilter(valores_baliza2_inter[j:j+numero_tramas])
      j=j+numero_tramas
      
valores_baliza3_inter=valores_baliza3_inter[:math.floor(len(valores_baliza3_inter)/numero_tramas)*numero_tramas]
j=0
for i in range (int(len(valores_baliza3_inter)/numero_tramas)):
      valores_baliza3_inter[j:j+numero_tramas] = KalmanFilter(valores_baliza3_inter[j:j+numero_tramas])
      j=j+numero_tramas

## Calculamos las distancias y las salas asociadas
sala = []
distancia = []
distancias = []
for i in range (len(valores_baliza1_inter)):
      if i>0:
            localizacion,distancia = calculo_sala(diccionario_fingerprints,valores_baliza1_inter[i],valores_baliza2_inter[i],valores_baliza3_inter[i],sala[len(sala)-1])
            sala = sala + [localizacion]
            distancias.append(distancia)
      else: 
            localizacion,distancia = calculo_sala(diccionario_fingerprints,valores_baliza1_inter[i],valores_baliza2_inter[i],valores_baliza3_inter[i],'Salon_3')
            sala = sala + [localizacion]
            distancias.append(distancia)
      i=i+1


dibujar_trayectoria(sala)
      
      
      
      