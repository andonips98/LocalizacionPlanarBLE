import matplotlib.pyplot as plt

import numpy as np

def dibujar_trayectoria(sala):
      
      ## Dibujo del recinto
      fig = plt.figure(1)
      
      plt.plot(np.zeros(103),np.arange(0,103),'k') ##Pared vertical externa izq
      
      plt.plot(np.ones(103)*22,np.arange(0,103),'k') ##Pared vertical a 2.2 m
      
      plt.plot(np.ones(10)*22,np.arange(52,62),'w') ##Pared vertical a 2.2 m
      
      plt.plot(np.ones(10)*22,np.arange(74,84),'w') ##Pared vertical a 2.2 m
      
      plt.plot(np.ones(32)*56,np.arange(0,32),'k') ##Pared vertical a 4.7 m
      
      plt.plot(np.ones(60)*72,np.arange(31,91),'k') ##Pared vertical a 7.2 m
      
      plt.plot(np.ones(10)*72,np.arange(36,46),'w') ##Pared vertical a 7.2 m
      
      plt.plot(np.ones(41)*9,np.arange(40,81),'k') ##Pared vertical a 1 m
      
      plt.plot(np.ones(10)*9,np.arange(50,60),'w') ##Pared vertical a 1 m
      
      
      plt.plot(np.ones(57)*92,np.arange(0,57),'k') ##Pared vertical externa derecha
      
      plt.plot(np.arange(0,93),np.zeros(93),'k') ##Pared horizontal inferior
      
      plt.plot(np.arange(22,93),np.ones(71)*31,'k') ##Pared horizontal a 3.1 m
      
      plt.plot(np.arange(28,38),np.ones(10)*31,'w') ##Pared horizontal a 3.1 m
      
      plt.plot(np.arange(60,70),np.ones(10)*31,'w') ##Pared horizontal a 3.1 m
      
      plt.plot(np.arange(0,10),np.ones(10)*40,'k') ##Pared horizontal a 4.7 m
      
      plt.plot(np.arange(18,23),np.ones(5)*40,'k') ##Pared horizontal a 4.7 m
      
      plt.plot(np.arange(22,73),np.ones(51)*67,'k') ##Pared horizontal a 6.7 m
      
      plt.plot(np.arange(72,93),np.ones(21)*56,'k') ##Pared horizontal a 5.6 m
      
      plt.plot(np.arange(0,10),np.ones(10)*80,'k') ##Pared horizontal a 8 m
      
      plt.plot(np.arange(22,72),np.ones(50)*67,'k') ##Pared horizontal a 6.7 m
      
      plt.plot(np.arange(22,73),np.ones(51)*90,'k') ##Pared horizontal a 9 m
      
      plt.plot(np.arange(0,23),np.ones(23)*102,'k') ##Pared horizontal superior
      
      plt.plot(np.arange(5,15),np.ones(10)*102,'w') ##Pared horizontal superior
      
      plt.plot(50,63,'cx',label='Módulo central') #Modulo central
      
      plt.plot(47,72,'bo',label='Baliza 1') #Baliza 1
      
      plt.plot(11,62,'ro', label='Baliza 2') #Baliza 2
      
      plt.plot(73,27,'go',label='Baliza 3') #Baliza 3
      
      
      plt.axis([-5,95,-5,135])
      plt.legend()
      plt.show()
      
      
      
      sala_anterior = 'Salon_4'
      for i in range(len(sala)):
            
            if sala_anterior != sala[i]:
                  
                  if sala[i]=='Salon_2':
                        plt.plot(59,55,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
      #                  plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Salon_4':
                        plt.plot(59,43,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
      #                  plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Pasillo_2':
                        plt.plot(16,68,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        #plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Cuarto3_2':
                        plt.plot(81,15,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        #plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Cuarto3_1':
                        plt.plot(66,15,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        #plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Cuarto2':
                        plt.plot(39,15,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        #plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Salon_3':
                        plt.plot(37,43,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        #plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Baño':
                        plt.plot(5,60,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        #plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Salon_1':
                        plt.plot(37,55,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
      #                  plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Cuarto1_1':
                        plt.plot(11,13,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        #plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Cocina_2':
                        plt.plot(59,79,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        #plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Entrada':
                        plt.plot(11,91,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        #plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Balcon':
                        plt.plot(82,43,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        #plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Cuarto1_2':
                        plt.plot(11,27,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        #plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Cocina_1':
                        plt.plot(39,79,'s')
                        fig.canvas.draw()
                        fig.canvas.flush_events()
      #                  plt.show()
      #                  sleep(1)
                  elif sala[i] == 'Pasillo_1':
                       plt.plot(16,53,'s')
                       fig.canvas.draw()
                       fig.canvas.flush_events()
      #                 plt.show()
      #                  sleep(1)
      
            sala_anterior = sala
      
#      
#      
#      
#      
#      
#      
#      