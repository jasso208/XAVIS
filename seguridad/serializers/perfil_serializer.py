from rest_framework import serializers
from seguridad.models.perfil import Perfil
class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['id','perfil','comentarios']