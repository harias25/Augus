import webbrowser

def func(error,param=False):
 
    #Declaración e inicilizacion de la variable "estática"
    if not hasattr(func,"listado"):
        func.listado = []

    if(param):
        func.listado = []
    else:
        if(error!=None):
            func.listado.append(error)
        else:
            return func.listado


class ReporteErrores():
    def generarReporte(self):
        listado = func(None)


        contenido = "<html>" + '\n' + "<head>" + '\n' + "<title>Reporte de Errores</title>" + '\n' + "</head>" + '\n'
        contenido = contenido + "<body bgcolor=\"black\">" + '\n' + "<center><Font size=22 color=darkred>" + "Reporte de Errores del Archivo del Proyecto" + "</Font></center>" + '\n'
        contenido = contenido + "<hr >" + '\n' + "<font color=white>" + '\n' + "<center>" + '\n'
        contenido = contenido + "<table border=1 align=center style=\"width:100%;\" >" + '\n'
        contenido = contenido + "<TR bgcolor=darkred>" + "\n"
        contenido = contenido + "<TH  style=\"font-size: 18px; width:20%; color:white\" align=center>Tipo de Error</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:30%; color:white\" align=center>Descripción del Error</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:10%; color:white\" align=center>Linea</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:10%; color:white\" align=center>Columna</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:10%; color:white\" align=center>Fecha</TH>" + '\n'
        contenido = contenido + "</TR>" + '\n'



        if(listado == None): listado = []

        for error in listado:
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" align=center>" + error.tipo + "</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + error.error + "</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + error.linea + "</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + error.columna + "</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + error.fechaHora + "</TD>" + '\n'
            contenido = contenido + "</TR>" + '\n'


        contenido = contenido + '\n' + "</center>" + '\n' + "</table>" + "</body>" + '\n' + "</html>"

        f = open ('reporteErrores.html','w')
        f.write(contenido)
        f.close()

        webbrowser.open_new_tab('reporteErrores.html')
        