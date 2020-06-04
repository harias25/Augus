class Entorno:
    def __init__(self,anterior):
        self.tabla = {}
        self.anterior = anterior

    def agregar(self, simbolo) :
        self.tabla[simbolo.id.lower()] = simbolo

    def obtenerLocal(self, id) :
        id = id.lower()
        if not id in self.tabla :
            return None

        return self.tabla[id]

    def existe(self,id):
        id = id.lower()
        sym = self.obtenerLocal(id)
        if(sym == None):
            sig = self.anterior
            while(sig != None):
                if not id in sig.tabla :
                    sym=None
                    sig = sig.siguiente
                else:
                    return True

        if(sym==None):
            return False
        else:
            return True

    def obtener(self,id):
        id = id.lower()
        sym = self.obtenerLocal(id)
        if(sym == None):
            sig = self.anterior
            while(sig != None):
                if not id in sig.tabla :
                    sym=None
                    sig = sig.siguiente
                else:
                    sym=sig.tabla[id]
                    break

        if(sym==None):
            return None
        else:
            return sym
            
    def eliminar(self,id):
        id = id.lower()
        sym = self.obtenerLocal(id)
        if(sym == None):
            sig = self.anterior
            while(sig != None):
                if not id in sig.tabla :
                    sig = sig.siguiente
                else:
                    del sig.tabla[id]
                    break
        else:
            del self.tabla[id]

    def reemplazar(self,simbolo):
        simbolo.id = simbolo.id.lower()
        sym = self.obtenerLocal(simbolo.id)
        if(sym == None):
            sig = self.anterior
            while(sig != None):
                if not simbolo.id in sig.tabla :
                    sig = sig.siguiente
                else:
                    sig.tabla[simbolo.id] = simbolo
                    break
        else:
            self.tabla[simbolo.id] = simbolo