from django.contrib import admin
from seguridad.models.seccion import Seccion
from seguridad.models.menu import Menu
from seguridad.models.permisos_usuario import Permisos_Usuario
from seguridad.models.user_2 import User_2
from seguridad.models.perfil import Perfil
from seguridad.models.permisos_perfil import PermisosPerfil

# Register your models here.
admin.site.register(Seccion)
admin.site.register(Menu)
admin.site.register(Permisos_Usuario) 
admin.site.register(User_2)
admin.site.register(Perfil)
admin.site.register(PermisosPerfil)