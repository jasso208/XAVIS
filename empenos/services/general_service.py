from empenos.models.dia_no_laboral import Dia_No_Laboral
from datetime import date, datetime, time,timedelta
from empenos.models.control_folios import Control_Folios
#valida que la fecha de vencimiento no caiga en algun dia de azueto, 
#en caso de caer en dia de azueto, le asigna el siguiente dia habil.
def fn_fecha_vencimiento_valida(fecha_vencimiento):
	try:
		#si el dia es de azueto, buscamos el siguiente hata encontrar un dia que no sea de azueto.
		dv=Dia_No_Laboral.objects.get(fecha=fecha_vencimiento)

		dia_mas = timedelta(days=1)
		#si la fecha de vencimiento existe en los dias inhabiles, buscamos el siguiente dia para que sea el de vencimiento.
		fecha_vencimiento=datetime.combine(fecha_vencimiento+dia_mas, time.min)

		dv=Dia_No_Laboral.objects.get(fecha=fecha_vencimiento)
		dia_mas = timedelta(days=1)

		#si la fecha de vencimiento existe en los dias inhabiles, buscamos el siguiente dia para que sea el de vencimiento.
		fecha_vencimiento=datetime.combine(fecha_vencimiento+dia_mas, time.min)

		dv=Dia_No_Laboral.objects.get(fecha=fecha_vencimiento)
		dia_mas = timedelta(days=1)

		#si la fecha de vencimiento existe en los dias inhabiles, buscamos el siguiente dia para que sea el de vencimiento.
		fecha_vencimiento=datetime.combine(fecha_vencimiento+dia_mas, time.min)

		dv=Dia_No_Laboral.objects.get(fecha=fecha_vencimiento)
		dia_mas = timedelta(days=1)

		#si la fecha de vencimiento existe en los dias inhabiles, buscamos el siguiente dia para que sea el de vencimiento.
		fecha_vencimiento=datetime.combine(fecha_vencimiento+dia_mas, time.min)

	except Exception as e:
		print(e)
		print("la fecha de vencimiento es valida")
	return  fecha_vencimiento


#funcion para generar folio de movimiento
def fn_folios(tipo_movimiento,sucursal):
	try:
		cf=Control_Folios.objects.get(tipo_movimiento=tipo_movimiento,sucursal=sucursal)
		folio=cf.folio+1
		cf.folio=folio
		cf.save()		
	except:
		#si no existe registro, crea uno
		Control_Folios.objects.create(tipo_movimiento=tipo_movimiento,sucursal=sucursal,folio=1)
		cf=Control_Folios.objects.get(tipo_movimiento=tipo_movimiento,sucursal=sucursal)
		folio=cf.folio
	return folio



def fn_str_clave(id):
	if len(str(id))==1:
		return '000000'+str(id)
	if len(str(id))==2:
		return '00000'+str(id)
	if len(str(id))==3:
		return '0000'+str(id)
	if len(str(id))==4:
		return '000'+str(id)
	if len(str(id))==5:
		return '00'+str(id)
	if len(str(id))==6:
		return '0'+str(id)
	if len(str(id))==7:
		return str(id)