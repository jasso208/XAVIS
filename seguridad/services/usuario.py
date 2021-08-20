from django.db import transaction
from django.db.transaction import atomic
import seguridad
from seguridad.models import permisos_perfil
from seguridad.models import perfil
from seguridad.models.permisos_usuario import Permisos_Usuario
from seguridad.models.permisos_perfil import PermisosPerfil
from seguridad.models.user_2 import User_2
from django.contrib.auth.models import User
from seguridad.models import Sucursal
from seguridad.models.perfil import Perfil
from django.utils import timezone

class UsuarioService():

    def consultaListaUsuarios():

        resp = []
        users = User_2.objects.all()
        print("jasso")
        print(users)
        for u in users:
            resp.append({"id":u.user.id,"username":u.user.username,"first_name":u.user.first_name,"last_name":u.user.last_name,"sucursal":u.sucursal.sucursal,"perfil":u.perfil.perfil,"activo":u.user.is_active})

        return resp
        
    def consultaUsuarioPorId(id_usuario):
        u = User.objects.get(id = id_usuario)
        u2 = User_2.objects.get(user = u)
        resp = {"username": u.username,"first_name":u.first_name,"last_name":u.last_name,"id_perfil":u2.perfil.id,"id_sucursal":u2.sucursal.id,"activo":u.is_active,"email":u.email}
        return resp


    def fn_alta_usuario(user_name,first_name,last_name,id_sucursal,id_perfil,id_usuario_alta,email):
        resp = []
        if user_name == "" or user_name == None:
            resp.append(False)
            resp.append("El nombre de usuario es requerido.")
            return resp

        try:
            sucursal = Sucursal.objects.get(id = id_sucursal)
        except:
            resp.append(False)
            resp.append("Debe indicar una sucursal valida.")
            return resp

        try:
            Perfil.objects.get(id = id_perfil)
        except:
            resp.append(False)
            resp.append("Debe indicar un perfil valido.")
            return resp


        usuario = User.objects.filter(username = user_name)

        if usuario.exists():
            resp.append(False)
            resp.append("El nombre de usuario indicado ya existe.")
            return resp


        
        with transaction.atomic():
            try:
                usuario_alta = User.objects.get(id = int(id_usuario_alta))
                usuario = User()
                usuario.username = user_name
                usuario.first_name = first_name.upper()
                usuario.last_name = last_name.upper()
                usuario.is_staff = True
                usuario.is_active = True
                usuario.email = email.upper()
                usuario.save()

                #Es la contraseña por default
                usuario.set_password("12345")
                usuario.save()
                
                user_2 = User_2()
                user_2.user = usuario
                user_2.sucursal = Sucursal.objects.get(id = int(id_sucursal))

                user_2.perfil = Perfil.objects.get(id = int(id_perfil))
                user_2.usuario_alta = usuario_alta
                user_2.save()

                c = UsuarioService.asigna_permisos_a_usuario(user_2,usuario_alta)                

                resp.append(True)
                resp.append("El usuario se creo correctamente.")
            except Exception as e:
                print(e)
                transaction.set_rollback(True)
                resp.append(False)
                resp.append("Error al crear el usuario, intente nuevamente.")
            
        return resp

    #asigna permisos al usuario en base al perfil que se le asigno.
    def asigna_permisos_a_usuario(user_2,usuario_alta):
        #borramos los permisos que actualmente tiene el usuario
        Permisos_Usuario.objects.filter(usuario = user_2.user).delete()

        #Buscamos las opciones a las que tiene acceso el perfil
        permisos_perfil = PermisosPerfil.objects.filter(perfil = user_2.perfil)
        try:
            for p in permisos_perfil:
                Permisos_Usuario.objects.create(usuario = user_2.user,opcion_menu = p.opcion,usuario_otorga = usuario_alta)
            return True
        except:
            return False

    def fn_edita_usuario(user_name,first_name,last_name,id_sucursal,id_perfil,id_usuario_alta,activo,email,password):
        
        resp = []
        if user_name == "" or user_name == None:
            resp.append(False)
            resp.append("El nombre de usuario es requerido.")
            return resp

        try:
            sucursal = Sucursal.objects.get(id = id_sucursal)
        except:
            resp.append(False)
            resp.append("Debe indicar una sucursal valida.")
            return resp

        try:
            Perfil.objects.get(id = id_perfil)
        except:
            resp.append(False)
            resp.append("Debe indicar un perfil valido.")
            return resp
			
        try:
            usr_modifica = User.objects.get(id = int(id_usuario_alta))

            usr_a_modificar = User.objects.get(username = user_name)

            u2 = User_2.objects.get(user = usr_a_modificar)

            if u2.fn_tiene_caja_abierta() != None:
                resp.append(False)
                resp.append("El usuario no puede ser modificado ya que cuenta con caja abierta.")
                return resp


            usr_a_modificar.first_name = first_name.upper()
            usr_a_modificar.last_name = last_name.upper()
            usr_a_modificar.email = email.upper()

            if activo == 0:
                usr_a_modificar.is_active = False
            else:				
                usr_a_modificar.is_active = True

            if password != "":#solo se modifica si nos envia un valor.
                usr_a_modificar.set_password(password)

            usr_a_modificar.save()


            user_2 = User_2.objects.get(user = usr_a_modificar)
            user_2.sucursal = Sucursal.objects.get(id = int(id_sucursal))
            user_2.perfil = Perfil.objects.get(id = int(id_perfil))
            user_2.usuario_modifica = usr_modifica
            user_2.fecha_modificacion = timezone.now()

            user_2.save()

            resp.append(True)
            resp.append("El usuario actualizo correctamente.")
        except Exception as e:
            print(e)
            resp.append(False)
            resp.append("Error al actualizar el usuario, intente nuevamente.")
            return resp

        return resp

    def editaPermisosUsuario(user,opcion,agrega_permiso,usuario_otorga):
                
        if agrega_permiso:
            try:
                Permisos_Usuario.objects.create(usuario = user,opcion_menu = opcion,usuario_otorga = usuario_otorga)
            except Exception as e:
                print(e)
                pass
        else:
            try:
                Permisos_Usuario.objects.get(usuario = user,opcion_menu = opcion).delete()
            except Exception as e:
                print(e)
                pass
        return True

    def cambiaPassword(user,password):
        try:
            user.set_password(password)
            user.save()
            return True
        except:
            return False
