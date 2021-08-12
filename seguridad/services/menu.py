from seguridad.models.seccion import Seccion
from seguridad.models.permisos_usuario import Permisos_Usuario
from seguridad.models.menu import Menu
class MenuService():

    def getOpcionesMenu():
        respuesta = []
        opciones = []
		
        secciones = Seccion.objects.all().order_by("orden")
        for s in secciones:
            #permisos = Permisos_Usuario.objects.filter(opcion_menu__seccion = s)

            op_aux = []#lista auxiliar que nos ayuda a ordenar los menus
            #for p in permisos:
             #   op_aux.append(p.opcion_menu.id)

            opciones = []
            for m in Menu.objects.filter(seccion = s).order_by("orden"):
                opciones.append({"id":m.id,"opcion":m.desc_item,"url_menu":m.url_menu,"visible":m.visible})
        
            glyphicon="glyphicon glyphicon-asterisk"
            if s.glyphicon != "":
                glyphicon = s.glyphicon
            respuesta.append({"id_seccion":s.id,"seccion":s.desc_seccion,"glyphicon":glyphicon,"opciones":opciones})
        return respuesta
