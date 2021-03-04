### Funcion para el calculo del filtro de Kalman
import numpy as np

def KalmanFilter(valores_originales):
    valores_filtrados = np.zeros(len(valores_originales)+1)
    valores_filtrados[0] = valores_originales[0]
    
    P_k = 1;
    R = 0.1;
    
    for i in range(len(valores_originales)):
        
        K_Ganancia = P_k/(P_k+R)
        valores_filtrados[i+1] = valores_filtrados[i] + K_Ganancia * (valores_originales[i] - valores_filtrados[i])
        P_k = (1 - K_Ganancia) * P_k
    
    return valores_filtrados[1::]