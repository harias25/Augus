import webbrowser
class ReporteTablaSimbolos():

    def generarReporte(self,ent,arbol):
        contenido = "<html>" + '\n' + "<head>" + '\n' + "<title>Reporte de Simbolos</title>" + '\n' + "</head>" + '\n'
        contenido = contenido + "<body bgcolor=\"black\">" + '\n' + "<center><Font size=22 color=darkred>" + "Reporte Tabla de Simbolos" + "</Font></center>" + '\n'
        contenido = contenido + "<hr >" + '\n' + "<font color=white>" + '\n' + "<center>" + '\n'
        contenido = contenido + "<table border=1 align=center style=\"width:100%;\" >" + '\n'
        contenido = contenido + "<TR bgcolor=darkred>" + "\n"
        contenido = contenido + "<TH  style=\"font-size: 18px; width:15%; color:white\" align=center>Tipo de Dato</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:20%; color:white\" align=center>ID</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:15%; color:white\" align=center>Ambito</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:15%; color:white\" align=center>Dimensión/Niveles</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:15%; color:white\" align=center>Valor</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:10%; color:white\" align=center>Linea</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:10%; color:white\" align=center>Columna</TH>" + '\n'
        

        for key in ent.tabla:
            try:
                s = ent.tabla[key]
                contenido = contenido + "<TR>"
                tipo = s.getTipo()
                contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + tipo + "</TD>" + '\n'
                contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + s.id + "</TD>" + '\n'
                contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + s.ambito + "</TD>" + '\n'
                if(isinstance(s.valor,dict)):
                    contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + str(len(s.valor)) +" / "+str(s.getNiveles(s.valor))+ "</TD>" + '\n'
                else:
                    contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" +"-" + "</TD>" + '\n'
                contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + str(s.valor) + "</TD>" + '\n'
                contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + str(s.linea)+ "</TD>" + '\n'
                contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + str(s.columna) + "</TD>" + '\n'
                contenido = contenido + "</TR>" + '\n'
            except:
                pass
            

        for etiqueta in arbol.etiquetas:
            contenido = contenido + "<TR>"
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>"+etiqueta.getTipo()+"</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + etiqueta.id + "</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>-</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>-</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>-</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + str(etiqueta.linea)+ "</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + str(etiqueta.columna) + "</TD>" + '\n'
            contenido = contenido + "</TR>" + '\n'

        contenido = contenido + '\n' + "</center>" + '\n' + "</table>" + "</body>" + '\n' + "</html>"

        f = open ('TablaSimbolos.html','w')
        f.write(contenido)
        f.close()

        webbrowser.open_new_tab('TablaSimbolos.html')