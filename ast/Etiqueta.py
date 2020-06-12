from ast.Instruccion import Instruccion
from ValorImplicito.Asignacion import Asignacion
import ast.Entorno as TS
import Primitivas.Exit as Exit
import Condicionales.If as If
import ast.GoTo as GoTo
import ValorImplicito.Asignacion as Asignacion
import ValorImplicito.Conversion as Conversion
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *

class Etiqueta(Instruccion) :
    def __init__(self,  id, instrucciones,linea,columna) :
        self.id = id
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol,ventana,isDebug):
        
        salir = False
        if(isDebug):
            QApplication.processEvents()
            ventana.editor.setCursorPosition(self.linea - 1,0)
            ventana.editor.setFocus()
            time.sleep(1)

        for ins in self.instrucciones:
            try:
                QApplication.processEvents()
                if(isDebug):
                    ventana.editor.setCursorPosition(ins.linea-1,0)
                    ventana.editor.setFocus()
                    time.sleep(1)

                if(isinstance(ins,Asignacion.Asignacion) or isinstance(ins,Conversion.Conversion)):
                    ins.setAmbito(self.id)
                if(ins.ejecutar(ent,arbol,ventana,isDebug) == True):
                    return True

                if(isDebug):
                    contador = 1
                    ventana.tableWidget.setRowCount(0)
                    ventana.tableWidget.setRowCount(100)
                    ventana.tableWidget.setItem(0,0, QTableWidgetItem("No."))
                    ventana.tableWidget.setItem(0,1, QTableWidgetItem("Simbolo"))
                    ventana.tableWidget.setItem(0, 2 , QTableWidgetItem("Valor"))
                    for key in ent.tabla:
                        QApplication.processEvents()
                        s = ent.tabla[key]
                        ventana.tableWidget.setItem(contador,0, QTableWidgetItem(str(contador)))
                        ventana.tableWidget.setItem(contador,1, QTableWidgetItem(s.id))
                        ventana.tableWidget.setItem(contador, 2 , QTableWidgetItem(str(s.valor)))
                        contador = contador + 1 

            except:
                pass

        if(not salir):
            siguiente = arbol.obtenerSiguienteEtiqueta(self.id)
            if(siguiente!=None):
                if(siguiente.ejecutar(ent,arbol,ventana,isDebug) == True):
                    return True
                
        return False

    def getTipo(self):
        isProc = False
        isFunc = False

        for ins in self.instrucciones:
            try:
                if(type(ins) is Asignacion):
                    if(ins.id.startswith('$a')):
                        isProc = True
                    
                    if(ins.id.startswith('$v')):
                        isFunc = True
                        break

            except:
                pass
            
        if(isFunc and isProc): return "FUNCION"
        if(isProc): return "PROCEDIMIENTO"
            
        return "ETIQUETA"