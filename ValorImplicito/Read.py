from ast.Instruccion import Instruccion
from ast.Declaracion import Declaracion
from ValorImplicito.Primitivo import Primitivo
from ValorImplicito.Asignacion import Asignacion
from ast.Simbolo import TIPO_DATO as Tipo
import Reporteria.Error as Error
import Reporteria.ReporteErrores as ReporteErrores
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *

class Read(Instruccion):
    def __init__(self,id,linea,columna):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.declarada = None

    def setAmbito(self,ambito):
        self.declarada = ambito

    def isfloat(self,x):
        try:
            a = float(x)
        except ValueError:
            return False
        else:
            return True

    def isint(self,x):
        try:
            a = float(x)
            b = int(a)
        except ValueError:
            return False
        else:
            return a == b

    def ejecutar(self,ent,arbol,ventana,isDebug):

        simbolo = ent.obtener(str(self.id))
        value = ""
        valorActual = ventana.consola.toPlainText()
        bandera = True

        while bandera:
            QApplication.processEvents()
            valorIngresado = ventana.consola.toPlainText()
            valorIngresado = valorIngresado.replace(valorActual,"")
            if(valorIngresado.endswith("\n")):
                value = valorIngresado.replace("\n","")
                bandera = False
        
        if(self.isint(value)):
            value = int(value)
        elif(self.isfloat(value)):
            value = float(value)
        
        if(simbolo == None):
            declarar = Declaracion(str(self.id),value,self.linea,self.columna,"",self.declarada)
            declarar.ejecutar(ent,arbol,ventana,isDebug)
        else:
            if(simbolo.puntero != ""):
                simboloP = ent.obtener(str(simbolo.puntero))
                simboloP.valor = value
                ent.reemplazar(simboloP)
            else:
                simbolo.valor = value
                ent.reemplazar(simbolo)
        
        return False 
    
