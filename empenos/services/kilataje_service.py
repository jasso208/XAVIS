from rest_framework.decorators import action
from rest_framework.views import APIView
from empenos.models import tipo_producto
from empenos.models import tipo_kilataje
from empenos.models.tipo_kilataje import Tipo_Kilataje
from empenos.models.tipo_producto import Tipo_Producto
from empenos.models.kilataje import Kilataje

class KilatajeService():

	def addKilataje(id_tipo_producto,id_tipo_kilataje,kilataje,avaluo):
		resp = {}
		try:
			tipo_producto = Tipo_Producto.objects.get(id = int(id_tipo_producto))
		except:
			resp = {"estatus":"0","msj":"El tipo de producto no es valido."}
			return resp

		try:
			tipo_kilataje = Tipo_Kilataje.objects.get(id = int(id_tipo_kilataje))
		except:
			resp = {"estatus":"0","msj":"El tipo de kilataje no es valido."}
			return resp
		if len(kilataje) > 10:
			resp = {"estatus":"0","msj":"La descripción del kilataje es demasiado grande. Máximo 10 caracteres."}
			return resp

		if avaluo < 0.01:
			resp = {"estatus":"0","msj":"EL importe de avalúo no es valido."}
			return resp

		try:
			Kilataje.objects.create(tipo_producto=tipo_producto,kilataje=kilataje,avaluo=avaluo,tipo_kilataje=tipo_kilataje)
		except:
			resp = {"estatus":"0","msj":"Error al guardar la informacion."}
			return resp

		resp = {"estatus":"1"}
		return resp

	def desactivaKilataje(id):
		kilataje = Kilataje.objects.get(id = id)
		kilataje.activo = "N"
		kilataje.save()
		return True

	#obtiene todos los kilatajes activos.
	def getAllKilatajes():
		resp = []
		kilatajes = Kilataje.objects.filter(activo = "S").order_by("kilataje")

		for k in kilatajes:
			
			resp.append({"id":k.id,"avaluo":k.avaluo,"id_tipo_producto":k.tipo_producto.id,"tipo_producto":k.tipo_producto.tipo_producto,"kilataje":k.kilataje,"id_tipo_kilataje":k.tipo_kilataje.id,"tipo_kilataje":k.tipo_kilataje.tipo_kilataje})

		return resp




			

