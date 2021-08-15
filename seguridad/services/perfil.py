from seguridad.models.permisos_perfil import PermisosPerfil
class PerfilService():

    def getPermisosPorPerfil(perfil):
        resp = []
        permisos = PermisosPerfil.objects.filter(perfil = perfil)
        for p in permisos:
            resp.append({"id":p.opcion.id,"opcion":p.opcion.desc_item})
        
        return resp

    #agrega o quita permisos a un perfil
    #parametros:
    #           Perfil: el perfil al que se le editaran los perfiles.
    #           opcion: La opcion el menu que se va a afectar
    #           agrega_permiso: true: agregar; false; quitar permiso de acceso a la opcion indicada.
    def editaPermisosPerfil(perfil,opcion,agrega_permiso):
        
        if agrega_permiso:
            try:
                PermisosPerfil.objects.create(perfil = perfil,opcion = opcion)
            except Exception as e:
                print(e)
                pass
        else:
            try:
                PermisosPerfil.objects.get(perfil = perfil,opcion = opcion).delete()
            except Exception as e:
                print(e)
                pass
        return True