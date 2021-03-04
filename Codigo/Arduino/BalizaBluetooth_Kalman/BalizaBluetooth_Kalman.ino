#include <ArduinoBLE.h>

// BLE Client Service
BLEService RaspberryRSSIService("fb36491d-7c21-40ef-9f67-a63237b5bbea");

// BLE Characteristic
BLEFloatCharacteristic RSSIMobileCharacteristic("fb36491e-7c21-40ef-9f67-a63237b5bbeb", BLERead | BLENotify);
BLEUnsignedLongCharacteristic SynNumberCharacteristic("fb36491e-7c21-40ef-9f67-a63237b5bbec", BLERead | BLENotify);
BLEUnsignedLongCharacteristic ComputoTimeCharacteristic("fb36491e-7c21-40ef-9f67-a63237b5bbed", BLERead | BLENotify);
BLEUnsignedIntCharacteristic IdPeripheralCharacteristic("fb36491e-7c21-40ef-9f67-a63237b5bbee", BLERead | BLENotify);

//Caracteristicas del bluetooth
float oldRSSILevel = 0;
long SynNumber = 0;
int Id = 0;
unsigned long computoTime = 0;

//Tiempos estimados
unsigned long previousComputoMillis = 0;
unsigned long currentMillis;
unsigned long previousMillis = 0;
unsigned long limite_millis = 0;
unsigned long limite_muestreo = 100;
unsigned long incremento_millis = 5;
unsigned long tiempoMaxPrev;
unsigned long tiempoMaxActual;  


//Indicadores
int IndRSSI;
int RSSI_Suma;
float RSSI_Media;
float ValorRSSI_anterior;

//Filtro de Kalman
float K_Ganancia = 0;
float P_k = 1;
float R = 0.1;

//Variables de iteracion
bool primerIter = true;

//Variables de estado de los perifericos
bool estadoConectado1 = false;
bool estadoConectado2 = false;
bool estadoConectado3 = false;
bool estadoConectado4 = false;
bool estadoConectado5 = false;

int Id1Conectado = 0;
int Id2Conectado = 0;
int Id3Conectado = 0;
int Id4Conectado = 0;
int Id5Conectado = 0;


void setup() {
  Serial.begin(19200);

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");
    while (1);
  }

  //Inicialización
  IndRSSI = 0;
  RSSI_Suma = 0;
  RSSI_Media = 0;

  //Servicio
  BLE.setLocalName("RSSIMonitor");
  BLE.setAdvertisedService(RaspberryRSSIService); 
  RaspberryRSSIService.addCharacteristic(RSSIMobileCharacteristic);
  RaspberryRSSIService.addCharacteristic(SynNumberCharacteristic); 
  RaspberryRSSIService.addCharacteristic(ComputoTimeCharacteristic);
  RaspberryRSSIService.addCharacteristic(IdPeripheralCharacteristic);   
  BLE.addService(RaspberryRSSIService); 
  RSSIMobileCharacteristic.writeValue(oldRSSILevel);
  SynNumberCharacteristic.writeValue(SynNumber);
  ComputoTimeCharacteristic.writeValue(computoTime);
  IdPeripheralCharacteristic.writeValue(Id);
  BLE.advertise();

  ///Sección de Central
  Serial.println("Servicio baliza Bluetooth en funcionamiento");
}

void loop() {

  BLEDevice central = BLE.central();

  BLEDevice peripheral_1;
  BLEDevice peripheral_2;
  BLEDevice peripheral_3;
  BLEDevice peripheral_4;
  BLEDevice peripheral_5;
  
  estadoConectado1 = false;
  estadoConectado2 = false;
  estadoConectado3 = false;
  estadoConectado4 = false;
  estadoConectado5 = false;

  //Conexión con la Raspberry
  if (central) {
    if (central.address() == "dc:a6:32:78:20:f7") {
      Serial.print("Baliza conectada a modulo principal. Dir.Bluetooth: ");
      Serial.println(central.address());
      Serial.println("Buscando dispositivos nuevos");
      BLE.scan(true);

      while (central.connected()) {
        tiempoMaxPrev = millis();

        if(!estadoConectado1)
          peripheral_1 = BLE.available();
          
        if(!estadoConectado2)
          peripheral_2 = BLE.available();
        
        if(!estadoConectado3)
          peripheral_3 = BLE.available();
          
        if(!estadoConectado4)
          peripheral_4 = BLE.available();
          
        if(!estadoConectado5)
          peripheral_5 = BLE.available();

        comprobarConectividad(peripheral_1, 1);
        comprobarConectividad(peripheral_2, 2);
        comprobarConectividad(peripheral_3, 3);
        comprobarConectividad(peripheral_4, 4);
        comprobarConectividad(peripheral_5, 5);                
        
        tiempoMaxActual = millis();
        Serial.print("Tiempo de ciclo: ");
        Serial.println(tiempoMaxActual - tiempoMaxPrev);
        BLE.scan(true);

      }

      peripheral_1.disconnect();
      peripheral_2.disconnect();
      peripheral_3.disconnect();
      peripheral_4.disconnect();
      peripheral_5.disconnect();

      Id1Conectado = 0;
      Id2Conectado = 0;
      Id3Conectado = 0;
      Id4Conectado = 0;
      Id5Conectado = 0;
      
      Id = 0;
      SynNumber = -1;
      updateRSSILevel("NO PERIFERICO", 0);

      central.disconnect();      
      Serial.print("Baliza desconectada del modulo principal. Dir.Bluetooth: ");
      Serial.println(central.address());
      BLE.stopScan();
      BLE.advertise();
    }
    else {
      Serial.println("Conectado dispositivo no deseado como central. Terminando conxión");
      Serial.print("Direccion del dispositivo: ");
      Serial.println(central.address());
      central.disconnect();
      BLE.advertise();
    }
  }

}

void updateRSSILevel(String peripheralAddress, int ValorRSSI) {
  
  computoTime = millis() - previousComputoMillis;

  if(peripheralAddress.equals("NO PERIFERICO"))
    computoTime = 0;

  SynNumber = SynNumber + 1;
  if(SynNumber > 1000)
    SynNumber = 0;
  
  
  Serial.print("Media RSSI del dispositivo ");
  Serial.print(peripheralAddress);
  Serial.print(" : ");
  Serial.println(ValorRSSI);
  Serial.println(SynNumber);
  Serial.println(computoTime);
  RSSIMobileCharacteristic.writeValue(ValorRSSI);
  SynNumberCharacteristic.writeValue(SynNumber);
  ComputoTimeCharacteristic.writeValue(computoTime);
  IdPeripheralCharacteristic.writeValue(Id); 
  
}

void comprobarConectividad(BLEDevice peripheral, int Id_){
  bool estadoConectado = false;
  bool EsUnPeriferico = false;

  if(Id_ == 1)
    estadoConectado = estadoConectado1;
  if(Id_ == 2)
    estadoConectado = estadoConectado2;
  if(Id_ == 3)
    estadoConectado = estadoConectado3;
  if(Id_ == 4)
    estadoConectado = estadoConectado4;   
  if(Id_ == 5)
    estadoConectado = estadoConectado5;

  if (peripheral) {
    Serial.println("Si hay periferico");

      if(peripheral.localName().equals("Periferico 1")){
        if(Id1Conectado == Id_ or Id1Conectado == 0){
          estadoConectado = estadoConectado1;
          Id1Conectado = Id_; 
          Id = 1;
          EsUnPeriferico = true;
          }
        }
      else if(peripheral.localName().equals("Periferico 2")){
        if(Id2Conectado == Id_ or Id2Conectado == 0){
          estadoConectado = estadoConectado2;
          Id2Conectado = Id_;
          Id = 2;
          EsUnPeriferico = true;
          }
        }  
      else if(peripheral.localName().equals("Periferico 3")){
        if(Id3Conectado == Id_ or Id3Conectado == 0){
          estadoConectado = estadoConectado3;
          Id3Conectado = Id_;
          Id = 3;
          EsUnPeriferico = true;
          }
        }    
      else if(peripheral.localName().equals("Periferico 4")){
        if(Id4Conectado == Id_ or Id4Conectado == 0){
          estadoConectado = estadoConectado4;
          Id4Conectado = Id_;
          Id = 4;
          EsUnPeriferico = true;
          }
        }    
      else if(peripheral.localName().equals("Periferico 5")){
        if(Id5Conectado == Id_ or Id5Conectado == 0){
          estadoConectado = estadoConectado5;
          Id5Conectado = Id_;
          Id = 5;
          EsUnPeriferico = true;
          }
        }

      if (EsUnPeriferico) {
        BLE.stopScan();
        //Si no esta conectado desde el inicio, intenta conectarse
        if (estadoConectado == false) {
          Serial.println("Conectando dispositivo");
          if (peripheral.connect()) {
            Serial.print("Dispositivo conectado - Address: ");
            Serial.println(peripheral.address());
            estadoConectado = true;
            }
          else
            Serial.println("Error al conectar dispositivo");
          }

          if (peripheral.connected())
            MonitoringDevice(peripheral, Id_);
          else {
            estadoConectado = false;       
            peripheral.disconnect();

            if(Id_ == 1 and Id1Conectado == Id_)
              Id1Conectado = 0;
            else if(Id_ == 2 and Id2Conectado == Id_)
              Id2Conectado = 0;
            else if(Id_ == 3 and Id3Conectado == Id_)
              Id3Conectado = 0;
            else if(Id_ == 4 and Id4Conectado == Id_)
              Id4Conectado = 0;
            else if(Id_ == 5 and Id5Conectado == Id_)
              Id5Conectado = 0;             
            
            Serial.println("Buscando periferico de nuevo...");
            }
            
          actualizarEstado(estadoConectado, Id_);
            
        }
    }
}

void actualizarEstado(bool estadoConectado, int Id_){

  if(Id_ == 1)
    estadoConectado1 = estadoConectado;
          
  if(Id_ == 2)
    estadoConectado2 = estadoConectado;
  
  if(Id_ == 3)
    estadoConectado3 = estadoConectado;
    
  if(Id_ == 4)
    estadoConectado4 = estadoConectado;
    
  if(Id_ == 5)
    estadoConectado5 = estadoConectado; 
}

void MonitoringDevice (BLEDevice peripheral, int Id_) {

  unsigned long dif_tiempo = 0;

  while(peripheral.connected() and dif_tiempo < limite_muestreo){
    currentMillis = millis();    

    if (primerIter == true) {
      previousMillis = currentMillis;
      primerIter = false;
      limite_millis = 0;
    }

    dif_tiempo = currentMillis - previousMillis;

    if ( dif_tiempo  >= limite_millis ) { //Cada cierto tiempo - Muestreo del RSSI
      
      float ValorRSSI = peripheral.rssi();
      
      if (IndRSSI == 0)
            ValorRSSI_anterior = 0;
            
      if (ValorRSSI != 0) {
        K_Ganancia = P_k/(P_k+R);
        ValorRSSI = ValorRSSI_anterior + K_Ganancia*(ValorRSSI-ValorRSSI_anterior);
        P_k=(1-K_Ganancia)*P_k;
        RSSI_Suma = RSSI_Suma + ValorRSSI;
        IndRSSI = IndRSSI + 1;
        ValorRSSI_anterior=ValorRSSI;
      }
      limite_millis = limite_millis + incremento_millis;
    }
    
  }

  if (IndRSSI != 0)
        RSSI_Media = RSSI_Suma / IndRSSI;
      else
        RSSI_Media = 0;

  IndRSSI = 0;
  RSSI_Suma = 0;
  P_k = 1;
  K_Ganancia = 0;
  previousComputoMillis = previousMillis;
  previousMillis = currentMillis;
  limite_millis = 0;
  primerIter = true;

  //Actualizacion de la media
  updateRSSILevel(peripheral.address(), RSSI_Media);

  if(!peripheral.connected()){
    Serial.print("Dispositivo ");
    Serial.print(peripheral.localName());
    Serial.println(" desconectado");

    if(Id_ == 1 and Id1Conectado == Id_)
      Id1Conectado = 0;
    else if(Id_ == 2 and Id2Conectado == Id_)
      Id2Conectado = 0;
    else if(Id_ == 3 and Id3Conectado == Id_)
      Id3Conectado = 0;
    else if(Id_ == 4 and Id4Conectado == Id_)
      Id4Conectado = 0;
    else if(Id_ == 5 and Id5Conectado == Id_)
      Id5Conectado = 0;
    
    actualizarEstado(false,Id_);
    Id = 0;
    SynNumber = -1;
    updateRSSILevel("NO PERIFERICO", 0);
    
    }
}
