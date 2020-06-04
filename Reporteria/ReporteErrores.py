def func(error):
 
    #Declaración e inicilizacion de la variable "estática"
    if not hasattr(func,"listado"):
        func.listado = []
        
    if(error!=None):
        func.listado.append(error)
    else:
        return func.listado


class ReporteErrores():
    def generarReporte(self):
        listado = func(None)
        if(listado == None): listado = []

        for error in listado:
                print(error.error)
                print("Tipo: "+error.tipo)
                print("Linea: "+error.linea)
                print("Columna: "+error.columna)
