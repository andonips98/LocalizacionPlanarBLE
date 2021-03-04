class tramaSeguimiento:
            
    def __init__(self,IdUser, MarcaTiempo):
        self.IdUser = IdUser
        self.MarcaTiempo = MarcaTiempo
        self.MarcaTiempoF = ''
        self.TiempoComputo1 = 0
        self.TiempoComputo2 = 0
        self.TiempoComputo3 = 0
        self.Tx1 = 0
        self.Tx2 = 0
        self.Tx3 = 0
        self.Lugar = ''

    def getIdUser(self):
        return self.IdUser        
        
    def getMarcaTiempo(self):
        return self.MarcaTiempo
    
    def getMarcaTiempoF(self):
        return self.MarcaTiempoF  
        
    def getTiempoComputo1(self):
        return self.TiempoComputo1
    
    def getTiempoComputo2(self):
        return self.TiempoComputo2
    
    def getTiempoComputo3(self):
        return self.TiempoComputo3    
        
    def getTx1(self):
        return self.Tx1
    
    def getTx2(self):
        return self.Tx2
    
    def getTx3(self):
        return self.Tx3
    
    def getLugar(self):
        return self.Lugar
    
    def getTx(self):
        Tx = [ self.Tx1, self.Tx2, self.Tx3]
        return Tx
    
    def getTiempoComputo(self):
        TiempoComputo = [ self.TiempoComputo1, self.TiempoComputo2, self.TiempoComputo3]
        return TiempoComputo
    
    
    def setIdUser(self, IdUser_):
        self.IdUser = IdUser_

    def setMarcaTiempo(self, MarcaTiempo_):
        self.MarcaTiempo = MarcaTiempo_
        
    def setMarcaTiempoF(self, MarcaTiempo_):
        self.MarcaTiempoF = MarcaTiempo_
        
    def setTiempoComputo1(self, TiempoComputo_):
        self.TiempoComputo1 = TiempoComputo_
        
    def setTiempoComputo2(self, TiempoComputo_):
        self.TiempoComputo2 = TiempoComputo_
        
    def setTiempoComputo3(self, TiempoComputo_):
        self.TiempoComputo3 = TiempoComputo_
    
    def setTx1(self, Tx1_):
        self.Tx1 = Tx1_
        
    def setTx2(self, Tx2_):
        self.Tx2 = Tx2_
        
    def setTx3(self, Tx3_):
        self.Tx3 = Tx3_
        
    def setLugar(self, Lugar_):
        self.Lugar = Lugar_
        
    def setTx(self, Tx):
        self.Tx1 = Tx[0]
        self.Tx2 = Tx[1]
        self.Tx3 = Tx[2]