import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *
import re
import time
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import tkinter as tk
from tkinter import filedialog
import ascendente as g
import AnalizadorDescendente.descendente as d
import ast.Entorno as TS
import ast.Instruccion as Instruccion
import ast.GoTo as GoTo
import ast.Declaracion as Declaracion
import Primitivas.Exit as Exit
import Condicionales.If as If
import ast.AST as AST
import Reporteria.Error as Error
import Reporteria.ReporteErrores as ReporteErrores
import Reporteria.ReporteTablaSimbolos as ReporteTablaSimbolos
import Reporteria.ReporteAST as ReporteAST
import ValorImplicito.Asignacion as Asignacion
import ValorImplicito.Conversion as Conversion
import Reporteria.ReporteGramatical as ReporteGramatical


class MyLexer(QsciLexerCustom):
    def __init__(self, parent):
        super(MyLexer, self).__init__(parent)
        # Configuración general del edito
        self.setDefaultColor(QColor("#ff000000"))  
        self.setDefaultPaper(QColor("#ffffffff"))
        self.setDefaultFont(QFont("Consolas", 12))

        #SE INICIALIZAN LOS COLORES POR ESTILOS
        self.setColor(QColor("#ff000000"), 0)                   # Estilo 0: negro   TEXTO EN GENERAL
        self.setColor(QColor("#ff7f0000"), 1)                   # Estilo 1: rojo    PALABRAS RESERVADAS
        self.setColor(QColor("#ff0000bf"), 2)                   # Estilo 2: azul    SIMBOLOS
        self.setColor(QColor("#ff007f00"), 3)                   # Estilo 3: verde   COMENTARIOS
        self.setColor(QColor(QColorConstants.DarkYellow), 4)    # Estilo 4: yellow  SIMBOLOS DE OPERACION
        self.setColor(QColor(QColorConstants.Magenta), 5)       # Estilo 5: Magenta NUMEROS
        self.setColor(QColor(QColorConstants.Gray), 6)          # Estilo 6: Gris    CADENAS
        self.setPaper(QColor("#ffffffff"), 0)   
        self.setPaper(QColor("#ffffffff"), 1)   
        self.setPaper(QColor("#ffffffff"), 2)   
        self.setPaper(QColor("#ffffffff"), 3)   
        self.setPaper(QColor("#ffffffff"), 4)   
        self.setPaper(QColor("#ffffffff"), 5)  
        self.setPaper(QColor("#ffffffff"), 6)  
        self.setFont(QFont("Consolas", 12), 0)   
        self.setFont(QFont("Consolas", 12, weight=QFont.Bold), 1)   
        self.setFont(QFont("Consolas", 12, weight=QFont.Bold), 2)   
        self.setFont(QFont("Consolas", 11, weight=QFont.Cursive), 3)
        self.setFont(QFont("Consolas", 12, weight=QFont.Bold), 4)   
        self.setFont(QFont("Consolas", 12, weight=QFont.DemiBold), 5)   
        self.setFont(QFont("Consolas", 12, weight=QFont.DemiBold), 6)  

    def language(self):
        return "SimpleLanguage"

    def description(self, style):
        if style == 0:
            return "myStyle_0"
        elif style == 1:
            return "myStyle_1"
        elif style == 2:
            return "myStyle_2"
        elif style == 3:
            return "myStyle_3"
        elif style == 4:
            return "myStyle_4"
        elif style == 5:
            return "myStyle_5"
        elif style == 6:
            return "myStyle_5"
        ###
        return ""

    def styleText(self, start, end):
        # 1. Initialize the styling procedure
        # ------------------------------------
        self.startStyling(start)

        # 2. Slice out a part from the text
        # ----------------------------------
        text = self.parent().text()[start:end]

        # 3. Tokenize the text
        # ---------------------
        p = re.compile(r"[*]\/|\/[*]|\s+|\w+|\W")

        # 'token_list' is a list of tuples: (token_name, token_len)
        token_list = [ (token, len(bytearray(token, "utf-8"))) for token in p.findall(text)]

        # 4. Style the text
        # ------------------
        # 4.1 Check if multiline comment
        comentario = False
        
        # 4.2 Style the text in a loop
        for i, token in enumerate(token_list):
            if comentario:
                if "\n" in str(token[0]):
                    comentario = False
                else:
                    self.setStyling(token[1], 3)
            else:
                if token[0] in ["int", "float", "char", "goto", "if","unset","print","read","array","exit","abs","xor"]:
                    self.setStyling(token[1], 1)
                elif token[0] in ["(", ")", ";", ":", "[", "]"]:
                    self.setStyling(token[1], 2)
                elif str(token[0]).isnumeric():
                    self.setStyling(token[1], 4)
                elif token[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
                    self.setStyling(token[1], 5)
                elif token[0] == "#":
                    comentario = True
                    self.setStyling(token[1], 3)
                else:
                    # Default style
                    self.setStyling(token[1], 0)
    
class Ui_MainWindow(object):

    resultChanged = QtCore.pyqtSignal(str)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1011, 738)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frameCodigo = QtWidgets.QFrame(self.centralwidget)
        self.frameCodigo.setGeometry(QtCore.QRect(0, 30, 661, 471))
        self.frameCodigo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameCodigo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameCodigo.setObjectName("frameCodigo")
        self.scrollDebug = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollDebug.setGeometry(QtCore.QRect(660, 30, 341, 471))
        self.scrollDebug.setWidgetResizable(False)
        self.scrollDebug.setObjectName("scrollDebug")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 339, 469))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 341, 471))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.scrollDebug.setWidget(self.scrollAreaWidgetContents)
        self.frameConsola = QtWidgets.QFrame(self.centralwidget)
        self.frameConsola.setGeometry(QtCore.QRect(0, 500, 1011, 211))
        self.frameConsola.setAutoFillBackground(True)
        self.frameConsola.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameConsola.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameConsola.setObjectName("frameConsola")
        self.consola = QtWidgets.QPlainTextEdit(self.frameConsola)
        self.consola.setGeometry(QtCore.QRect(10, 0, 991, 211))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)


        font2 = QtGui.QFont()
        font2.setFamily("Consolas")
        font2.setPointSize(13)
        font2.setBold(True)
        font2.setWeight(100)
        font2.setKerning(True)


        self.consola.setFont(font2)
        self.consola.setAutoFillBackground(False)
        #self.consola.setTextFormat(QtCore.Qt.RichText)
        self.consola.setObjectName("consola")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-1, 0, 1001, 31))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1011, 21))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuPrograma = QtWidgets.QMenu(self.menubar)
        self.menuPrograma.setObjectName("menuPrograma")
        self.menuReportes = QtWidgets.QMenu(self.menubar)
        self.menuReportes.setObjectName("menuReportes")
        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNuevo = QtWidgets.QAction(MainWindow)
        self.actionNuevo.setObjectName("actionNuevo")
        self.actionArbir = QtWidgets.QAction(MainWindow)
        self.actionArbir.setObjectName("actionArbir")
        self.actionGuardar = QtWidgets.QAction(MainWindow)
        self.actionGuardar.setObjectName("actionGuardar")
        self.actionGuardar_Como = QtWidgets.QAction(MainWindow)
        self.actionGuardar_Como.setObjectName("actionGuardar_Como")
        self.actionCerrrar = QtWidgets.QAction(MainWindow)
        self.actionCerrrar.setObjectName("actionCerrrar")
        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.actionCopiar = QtWidgets.QAction(MainWindow)
        self.actionCopiar.setObjectName("actionCopiar")
        self.actionPegar = QtWidgets.QAction(MainWindow)
        self.actionPegar.setObjectName("actionPegar")
        self.actionCortar = QtWidgets.QAction(MainWindow)
        self.actionCortar.setObjectName("actionCortar")
        self.actionBuscar = QtWidgets.QAction(MainWindow)
        self.actionBuscar.setObjectName("actionBuscar")
        self.actionReemplazar = QtWidgets.QAction(MainWindow)
        self.actionReemplazar.setObjectName("actionReemplazar")
        self.actionEjecutar_Descendente = QtWidgets.QAction(MainWindow)
        self.actionEjecutar_Descendente.setObjectName("actionEjecutar_Descendente")
        self.actionEjecutar_Ascendente = QtWidgets.QAction(MainWindow)
        self.actionEjecutar_Ascendente.setObjectName("actionEjecutar_Ascendente")
        self.actionEjecutar_Paso_a_Paso_Ascendente = QtWidgets.QAction(MainWindow)
        self.actionEjecutar_Paso_a_Paso_Ascendente.setObjectName("actionEjecutar_Paso_a_Paso_Ascendente")
        self.actionTabla_de_Simbolos = QtWidgets.QAction(MainWindow)
        self.actionTabla_de_Simbolos.setObjectName("actionTabla_de_Simbolos")
        self.actionErrores = QtWidgets.QAction(MainWindow)
        self.actionErrores.setObjectName("actionErrores")
        self.actionAST = QtWidgets.QAction(MainWindow)
        self.actionAST.setObjectName("actionAST")
        self.actionGramatical = QtWidgets.QAction(MainWindow)
        self.actionGramatical.setObjectName("actionGramatical")

        self.actionAyuda = QtWidgets.QAction(MainWindow)
        self.actionAyuda.setObjectName("actionAyuda")
        self.actionAcercaDe = QtWidgets.QAction(MainWindow)
        self.actionAcercaDe.setObjectName("actionAcercaDe")

        self.menuArchivo.addAction(self.actionNuevo)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionArbir)
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuArchivo.addAction(self.actionGuardar_Como)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionCerrrar)
        self.menuArchivo.addAction(self.actionSalir)
        self.menuPrograma.addAction(self.actionEjecutar_Descendente)
        self.menuPrograma.addSeparator()
        self.menuPrograma.addAction(self.actionEjecutar_Ascendente)
        self.menuPrograma.addAction(self.actionEjecutar_Paso_a_Paso_Ascendente)
        self.menuReportes.addAction(self.actionTabla_de_Simbolos)
        self.menuReportes.addAction(self.actionErrores)
        self.menuReportes.addAction(self.actionAST)
        self.menuReportes.addAction(self.actionGramatical)
        self.menuAyuda.addAction(self.actionAyuda)
        self.menuAyuda.addAction(self.actionAcercaDe)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuPrograma.menuAction())
        self.menubar.addAction(self.menuReportes.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())


        self.__myFont = QFont()
        self.__myFont.setPointSize(12)
        #************************************************ REGLAS DEL LENGUAJE AUGUS *****************************************
        self.editor = QsciScintilla()
        self.editor.setText("")              
        self.editor.setLexer(None)           
        self.editor.setUtf8(True)             
        self.editor.setFont(self.__myFont)    

        #AJUSTES DE TEXTO
        self.editor.setWrapMode(QsciScintilla.WrapWord)
        self.editor.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
        self.editor.setWrapIndentMode(QsciScintilla.WrapIndentIndented)

        #FIN DE LINEA
        self.editor.setEolMode(QsciScintilla.EolWindows)
        self.editor.setEolVisibility(False)

        #SANGRIA
        self.editor.setIndentationsUseTabs(False)
        self.editor.setTabWidth(4)
        self.editor.setIndentationGuides(True)
        self.editor.setTabIndents(True)
        self.editor.setAutoIndent(True)

        self.editor.setCaretForegroundColor(QColor("#ff0000ff"))
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor("#1f0000ff"))
        self.editor.setCaretWidth(2)

        # MARGENES
        self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.editor.setMarginWidth(0, "0000")  #con este se puede quitar la linea
        self.editor.setMarginsForegroundColor(QColor("#ff888888"))

        #SE COLOCAN LAS REGLAS DEL EDITOR
        self.__lexer = QsciLexerRuby(self.editor)
        self.editor.setLexer(self.__lexer)

        self.__lyt = QVBoxLayout()
        self.frameCodigo.setLayout(self.__lyt)
        self.__lyt.addWidget(self.editor)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionNuevo.triggered.connect(self.clean)
        self.actionArbir.triggered.connect(self.open)
        self.actionGuardar.triggered.connect(self.save)
        self.actionGuardar_Como.triggered.connect(self.save_as)
        self.actionCerrrar.triggered.connect(self.clear)
        self.actionSalir.triggered.connect(self.exit)
        self.ruta_archivo  = None
        self.actionEjecutar_Ascendente.triggered.connect(self.ascendente)
        self.actionEjecutar_Descendente.triggered.connect(self.descendente)
        self.actionTabla_de_Simbolos.triggered.connect(self.generarTabla)
        self.actionErrores.triggered.connect(self.generarRErrores)
        self.actionGramatical.triggered.connect(self.generarRGramatical)
        self.actionAST.triggered.connect(self.generarAST)

        self.actionAcercaDe.triggered.connect(self.acercade)
        self.actionAyuda.triggered.connect(self.ayuda)

        self.ts_global = TS.Entorno(None)
        self.ast =  AST.AST([]) 
        self.listado_gramatical = []
        self.instrucciones = []
        self.hilo_terminado = True
        self.actionEjecutar_Paso_a_Paso_Ascendente.triggered.connect(self.debugger)


        self.tableWidget.setRowCount(100)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setItem(0,0, QTableWidgetItem("No."))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Simbolo"))
        self.tableWidget.setItem(0, 2 , QTableWidgetItem("Valor"))

        self.tableWidget.setColumnWidth(0, 10)
        self.tableWidget.setColumnWidth(1, 75)
        self.tableWidget.setColumnWidth(2, 175)

        self.consola.setStyleSheet("background-color: black;border: 1px solid black;color:green;") 
        #self.consola.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

    def clean(self):
        self.ruta_archivo = None
        self.editor.setText("")
        self.consola.clear()

    def acercade(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("AUGUS IDE\nPrimer Proyecto Compiladores 2 Vacaciones Junio\nElaborado por: Haroldo Arias\nCarnet: 201020247")
        msg.setInformativeText("Python 3.8.3\nPLY\nPyQT\nScintilla")
        msg.setWindowTitle("Acerca de")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def ayuda(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("AUGUS IDE")
        msg.setInformativeText("Puedes encontrar el manual de este proyecto en:\nhttps://tinyurl.com/yabg9why")
        msg.setWindowTitle("Ayuda")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def setTexto(self,texto):
        self.consola.setText(self.consola.text() + texto)

    def generarAST(self):
        reporteAST = ReporteAST.ReporteAST()
        reporteAST.graficar(self.instrucciones)

    def generarTabla(self):
        reporteTablas = ReporteTablaSimbolos.ReporteTablaSimbolos()
        reporteTablas.generarReporte(self.ts_global,self.ast)

    def generarRErrores(self):
        reporteErrores = ReporteErrores.ReporteErrores()
        reporteErrores.generarReporte()

    def generarRGramatical(self):
        listado = self.listado_gramatical 
        reporteGramatical = ReporteGramatical.ReporteGramatical()
        reporteGramatical.generarReporte(listado[0])

    def debugger(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(100)
        self.tableWidget.setItem(0,0, QTableWidgetItem("No."))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Simbolo"))
        self.tableWidget.setItem(0, 2 , QTableWidgetItem("Valor"))



        if(self.hilo_terminado):
            sys.setrecursionlimit(2147483644)
            self.consola.clear()
            ReporteErrores.func(None,True)
            g.func(0,None)
            g.textoEntrada = self.editor.text()
            instrucciones = g.parse(self.editor.text())
            self.instrucciones = instrucciones
            ts_global = TS.Entorno(None)
            ast = AST.AST(instrucciones) 

            declaracion1 = Declaracion.Declaracion('$ra',0,0,0,"","GLOBAL")
            declaracion2 = Declaracion.Declaracion('$sp',0,0,0,"","GLOBAL")
            declaracion1.ejecutar(ts_global,ast,self,True)
            declaracion2.ejecutar(ts_global,ast,self,True)

            bandera = False
            if(instrucciones != None):
                for ins in instrucciones:
                    try:
                        if(bandera == False and ins.id != "main"):
                            error = Error.Error("SEMANTICO","Error semantico, La primera etiqueta debe ser la etiqueta main:",ins.linea,ins.columna)
                            ReporteErrores.func(error)
                            break
                        else:
                            bandera = True
                        if(ast.existeEtiqueta(ins)):
                            error = Error.Error("SEMANTICO","Error semantico, Ya existe la etiqueta "+ins.id,ins.linea,ins.columna)
                            ReporteErrores.func(error)
                        else:
                            ast.agregarEtiqueta(ins)
                    except:
                            pass
            self.ts_global = ts_global
            self.ast = ast
            self.listado_gramatical = g.func(1,None).copy()

            self.debug()

    def descendente(self):
        sys.setrecursionlimit(2147483644)
        self.consola.clear()
        d.textoEntrada = self.editor.text()
        d.band(1,False)
        ReporteErrores.func(None,True)
        d.func(0,None)
        instrucciones = d.parse(self.editor.text())
        self.instrucciones = instrucciones
        ts_global = TS.Entorno(None)
        ts_global.asignarConsola(self.consola)
        ast = AST.AST(instrucciones) 

        declaracion1 = Declaracion.Declaracion('$ra',0,0,0,"","GLOBAL")
        declaracion2 = Declaracion.Declaracion('$sp',0,0,0,"","GLOBAL")
        declaracion1.ejecutar(ts_global,ast,self,False)
        declaracion2.ejecutar(ts_global,ast,self,False)


        #PRIMERA PASADA PARA GUARDAR TODAS LAS ETIQUETAS
        bandera = False
        if(instrucciones != None):
            for ins in instrucciones:
                try:
                    if(bandera == False and ins.id != "main"):
                        error = Error.Error("SEMANTICO","Error semantico, La primera etiqueta debe ser la etiqueta main:",ins.linea,ins.columna)
                        ReporteErrores.func(error)
                        break
                    else:
                        bandera = True
                    if(ast.existeEtiqueta(ins)):
                        error = Error.Error("SEMANTICO","Error semantico, Ya existe la etiqueta "+ins.id,ins.linea,ins.columna)
                        ReporteErrores.func(error)
                    else:
                        ast.agregarEtiqueta(ins)
                except:
                        pass

        main = ast.obtenerEtiqueta("main")

        if(main != None):
            salir = False
            for ins in main.instrucciones:
                try:
                    if(isinstance(ins,Asignacion.Asignacion) or isinstance(ins,Conversion.Conversion)):
                        ins.setAmbito("main")

                    if(ins.ejecutar(ts_global,ast,self,False) == True):
                        salir = True
                        break
                except:
                    pass
            if(not salir):   
                siguiente = ast.obtenerSiguienteEtiqueta("main")
                if(siguiente!=None):
                    siguiente.ejecutar(ts_global,ast,self,False)
        else:
            error = Error.Error("SEMANTICO","Error semantico, No puede iniciarse el programa ya que no existe la etiqueta main:",0,0)
            ReporteErrores.func(error)

        listado = ReporteErrores.func(None)
        if(len(listado)>0):
            QMessageBox.critical(self.centralwidget, "Errores en Ejecución", "Se obtuvieron errores en la ejecución del Código Ingresado, verifique reporte de Errores")

        self.ts_global = ts_global
        self.ast = ast
        self.listado_gramatical = d.func(1,None).copy()

    def ascendente(self):
        sys.setrecursionlimit(2147483644)
        self.consola.clear()
        ReporteErrores.func(None,True)
        g.textoEntrada = self.editor.text()
        g.func(0,None)
        instrucciones = g.parse(self.editor.text())
        self.instrucciones = instrucciones
        ts_global = TS.Entorno(None)
        ts_global.asignarConsola(self.consola)
        ast = AST.AST(instrucciones) 

        declaracion1 = Declaracion.Declaracion('$ra',0,0,0,"","GLOBAL")
        declaracion2 = Declaracion.Declaracion('$sp',0,0,0,"","GLOBAL")
        declaracion1.ejecutar(ts_global,ast,self,False)
        declaracion2.ejecutar(ts_global,ast,self,False)


        #PRIMERA PASADA PARA GUARDAR TODAS LAS ETIQUETAS
        bandera = False
        if(instrucciones != None):
            for ins in instrucciones:
                try:
                    if(bandera == False and ins.id != "main"):
                        error = Error.Error("SEMANTICO","Error semantico, La primera etiqueta debe ser la etiqueta main:",ins.linea,ins.columna)
                        ReporteErrores.func(error)
                        break
                    else:
                        bandera = True
                    if(ast.existeEtiqueta(ins)):
                        error = Error.Error("SEMANTICO","Error semantico, Ya existe la etiqueta "+ins.id,ins.linea,ins.columna)
                        ReporteErrores.func(error)
                    else:
                        ast.agregarEtiqueta(ins)
                except:
                        pass

        main = ast.obtenerEtiqueta("main")

        if(main != None):
            salir = False
            for ins in main.instrucciones:
                try:
                    if(isinstance(ins,Asignacion.Asignacion) or isinstance(ins,Conversion.Conversion)):
                        ins.setAmbito("main")

                    if(ins.ejecutar(ts_global,ast,self,False) == True):
                        salir = True
                        break
                except:
                    pass
            if(not salir):   
                siguiente = ast.obtenerSiguienteEtiqueta("main")
                if(siguiente!=None):
                    siguiente.ejecutar(ts_global,ast,self,False)
        else:
            error = Error.Error("SEMANTICO","Error semantico, No puede iniciarse el programa ya que no existe la etiqueta main:",0,0)
            ReporteErrores.func(error)

        listado = ReporteErrores.func(None)
        if(len(listado)>0):
            QMessageBox.critical(self.centralwidget, "Errores en Ejecución", "Se obtuvieron errores en la ejecución del Código Ingresado, verifique reporte de Errores")

        self.ts_global = ts_global
        self.ast = ast
        self.listado_gramatical = g.func(1,None).copy()

    def debug(self):
        self.hilo_terminado = False
        main = self.ast.obtenerEtiqueta("main")

        if(main != None):
            salir = False
            self.editor.setCursorPosition(0,0)
            self.editor.setFocus()
            time.sleep(2)
            for ins in main.instrucciones:
                QApplication.processEvents()
                try:
                    self.editor.setCursorPosition(ins.linea-1,0)
                    self.editor.setFocus()
                    time.sleep(2)
                    if(isinstance(ins,Asignacion.Asignacion) or isinstance(ins,Conversion.Conversion)):
                        ins.setAmbito("main")
                    if(ins.ejecutar(self.ts_global,self.ast,self,True) == True):
                        salir = True
                        break
                    
                    contador = 1
                    for key in self.ts_global.tabla:
                        s = self.ts_global.tabla[key]
                        self.tableWidget.setItem(contador,0, QTableWidgetItem(str(contador)))
                        self.tableWidget.setItem(contador,1, QTableWidgetItem(s.id))
                        self.tableWidget.setItem(contador, 2 , QTableWidgetItem(str(s.valor)))
                        contador = contador + 1 
                    
                    
                except:
                    pass
            
            if(not salir):   
                siguiente = self.ast.obtenerSiguienteEtiqueta("main")
                if(siguiente!=None):
                    siguiente.ejecutar(self.ts_global,self.ast,self,True)
        else:
            error = Error.Error("SEMANTICO","Error semantico, No puede iniciarse el programa ya que no existe la etiqueta main:",0,0)
            ReporteErrores.func(error)
        listado = ReporteErrores.func(None)
        if(len(listado)>0):
            QMessageBox.critical(self.centralwidget, "Errores en Ejecución", "Se obtuvieron errores en la ejecución del Código Ingresado, verifique reporte de Errores")
        self.hilo_terminado = True
        #print ("Terminado hilo ")

    def exit(self):
        sys.exit()

    def clear(self):
        self.ruta_archivo = None
        self.editor.setText("")

    def open(self):
        root = tk.Tk()
        root.withdraw()
        ruta = filedialog.askopenfilename(title="Seleccione un archivo de Entrada")
        if not ruta: return
        try:
            f = open(ruta,"r")
            input = f.read()
            self.editor.setText(input)
            f.close()
            self.ruta_archivo = ruta
        except Exception as e:
            raise
            QMessageBox.critical(self.centralwidget,'Error Cargando el Archivo', 'No es posible abrir el archivo: %r' % ruta)

    def save(self):
        if(self.ruta_archivo==None):
            root = tk.Tk()
            root.withdraw()
            ruta = filedialog.asksaveasfilename(title="Seleccione la ruta donde desea guardar el Archivo",filetypes=[('all files', '.*'), ('text files', '.txt')])
        else:
            ruta = self.ruta_archivo
        if not ruta: return
        try:
            f = open(ruta,"w")
            f.write(self.editor.text())
            f.close()
        except Exception as e:
            raise
            QMessageBox.critical(self.centralwidget,'Error Guardando el Archivo', 'No es posible guardar el archivo: %r' % ruta)

    def save_as(self):
        ruta = filedialog.asksaveasfilename(title="Seleccione la ruta donde desea guardar el Archivo",filetypes=[('all files', '.*'), ('text files', '.txt')])
        if not ruta: return
        try:
            f = open(ruta,"w")
            f.write(self.editor.text())
            f.close()
            self.ruta_archivo = ruta
        except Exception as e:
            raise
            QMessageBox.critical(self.centralwidget,'Error Guardando el Archivo', 'No es posible guardar el archivo: %r' % ruta)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IDE AUGUS - HAROLDO PABLO ARIAS MOLINA - 201020247"))
        #self.consola.setText(_translate("MainWindow", ""))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuPrograma.setTitle(_translate("MainWindow", "Programa"))
        self.menuReportes.setTitle(_translate("MainWindow", "Reportes"))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda"))
        self.actionNuevo.setText(_translate("MainWindow", "Nuevo"))
        self.actionArbir.setText(_translate("MainWindow", "Abrir"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar_Como.setText(_translate("MainWindow", "Guardar Como"))
        self.actionCerrrar.setText(_translate("MainWindow", "Cerrrar"))
        self.actionSalir.setText(_translate("MainWindow", "Salir"))

        self.actionEjecutar_Descendente.setText(_translate("MainWindow", "Ejecutar Descendente"))
        self.actionEjecutar_Ascendente.setText(_translate("MainWindow", "Ejecutar Ascendente"))
        self.actionEjecutar_Paso_a_Paso_Ascendente.setText(_translate("MainWindow", "Ejecutar Paso a Paso Ascendente"))
        self.actionTabla_de_Simbolos.setText(_translate("MainWindow", "Tabla de Simbolos"))
        self.actionErrores.setText(_translate("MainWindow", "Errores"))
        self.actionAST.setText(_translate("MainWindow", "AST"))
        self.actionGramatical.setText(_translate("MainWindow", "Gramatical"))

        self.actionAyuda.setText(_translate("MainWindow", "Ayuda"))
        self.actionAcercaDe.setText(_translate("MainWindow", "Acerca de"))

interfaz = None

def getUI():
    global interfaz
    return interfaz.consola

if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10**9)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowFlags(MainWindow.windowFlags() | QtCore.Qt.CustomizeWindowHint)
    MainWindow.setWindowFlags(MainWindow.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    interfaz = ui
    MainWindow.show()
    sys.exit(app.exec_())


