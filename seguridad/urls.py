from django.conf.urls import url

from seguridad.api_rest.login import LoginApi
from seguridad.api_rest.permisos_usuario import PermisosUsuarioApi
from seguridad.api_rest.perfil import PerfilApi
from seguridad.api_rest.menu import MenuApi
from seguridad.api_rest.user import UsuarioApi
from seguridad.api_rest.sucursal import SucursalApi
app_name="seguridad"

urlpatterns=[

	#*****************************************************************************************************************
	#De aqui para abajo es para la migracion
	url(r'^v2/inicia_session/$',LoginApi.as_view()),
	url(r'^v2/cerrar_session/(?P<token>\w+)/',LoginApi.as_view()),
	url(r'^v2/permisos/$',PermisosUsuarioApi.as_view()),	
	url(r'^v2/perfiles/$',PerfilApi.as_view()),	
	url(r'^v2/menu/$',MenuApi.as_view()),	
	url(r'^v2/usuarios/$',UsuarioApi.as_view()),
	url(r'^v2/sucursales/$',SucursalApi.as_view())


]



