from django.db import models
from rest_framework import fields, serializers
from seguridad.models.permisos_usuario import Permisos_Usuario
class PermisosUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permisos_Usuario
        fields = ['menu','idSeccion']