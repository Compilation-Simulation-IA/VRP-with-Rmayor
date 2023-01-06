# Editor de texto
# Requisitos:
#   - appjar: http://appjar.info/
import sys
import time
from appJar import gui


######################
#      Funciones     #
######################
class utils:
	
    name = "Simple Text app"
    
    size = "600x500"
    
    # reloj
    def showTime():
        app.setStatusbar(time.strftime("%X"))

    # botones navegacion
    def menuPress(btn):
        if btn == "Abrir":
            # contenido textarea
            fileName = app.openBox(
                title="Abir Archivo", 
                dirName=None, 
                fileTypes=None, 
                # true hace que retorne la lista 
                # con el nombre del archivo
                asFile=True, 
                parent=None
            )
            # abrimos el archivo
            readFile = open(fileName.name,"r")
            # vaciamos textarea
            app.clearTextArea("t1")
            # insertamos el texto
            app.setTextArea("t1", readFile.read())
        elif btn == "Guardar":
            # content
            fileName = app.saveBox(
                title="Guardar Archivo", 
                fileName=None, 
                dirName=None, 
                fileExt=None, 
                fileTypes=None,
                # true hace que retorne 
                #la lista con el nombre del archivo
                asFile=True, 
                parent=None
            )
            try:
                # abrimos el archivo en modo write
                readFile = open(fileName.name,"w")
                # escribimos el archivo
                readFile.write(app.getTextArea("t1")) 
                # cerramos		
                readFile.close()
            except:
                pass

        elif btn == "Cerrar":
            app.stop()
                    
    # boton acerca de
    def aboutPress(btn):
        if btn == "Acerca de":
            textoAbout = """App creada por Moncho varela \n mas info https://monchovarela.es"""
            app.infoBox("Acerca Del Author", textoAbout)

    # navegacion
    def mainNav():
        # creamos menu
        navigation = ["Abrir", "Guardar","-", "Cerrar"]
        app.addMenuList("Archivo", navigation, utils.menuPress)

        fileMenus = ["Acerca de"]
        app.addMenuList("Ayuda", fileMenus, utils.aboutPress)


    # Editor
    def mainInit():
        # insertamos textareaa
        app.addScrolledTextArea("t1")
        ## insertamos el primer texto
        app.setTextArea("t1", "Emezamos ....")
        # color fondo
        app.setTextAreaBg("t1",'blue')
        # color texto
        app.setTextAreaFg("t1",'white')
        # font-size
        app.setFont('12')
        # padding
        app.setTextAreaPadding("t1",[20,20])


    # main footer
    def mainFooter():
        # reloj en el footer
        app.addStatusbar(side="RIGHT")
        app.registerEvent(utils.showTime)


#########################
#       Aplicacion      #
#########################

# iniciamos la ventana
app = gui(utils.name,utils.size)

# iniciamos navigation
utils.mainNav()
# iniciamos textarea
utils.mainInit()
# iniciamos footer
utils.mainFooter()

# lanzamos la aplicacion
app.go()