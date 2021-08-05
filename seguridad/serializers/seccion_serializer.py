from rest_framework import fields, serializers
from seguridad.models.seccion import Seccion

class SeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seccion
        fields = ['id','desc_seccion']
