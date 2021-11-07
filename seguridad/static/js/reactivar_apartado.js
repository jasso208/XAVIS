var csrf_token="";
var username="";
var ip_local="";
$(document).ready(
    function(){

        $(".cls_ayuda").hide();        
        $(".cls_msj_aviso").hide();
        $("#fondo_preloader").hide();
        $("#btn_ayuda").click(
            function(){
                $(".cls_ayuda").show();
            }
        );
        $("#btn_aceptar_ayuda").click(
            function(){
                $(".cls_ayuda").hide();        
            }
        );
        $("#btn_guardar").click(
            function(){
                reactivaApartado();
            }
        );
        $("#btn_aceptar_aviso").click(
            function(){
                $(".cls_msj_aviso").hide();
            }
        );
    }
);

function inicio(token,un,ip){
    csrf_token = token;
	username = un;
	ip_local = ip;
}
function reactivaApartado(){
    if (validaFormulario()){
        var dataVal = {};

        dataVal["folioApartado"] = $("#id_folio_apartado").val();
        dataVal["idSucursal"] = $("#id_sucursal").val();
        dataVal["folioBoleta"] = $("#id_folio_boleta").val();
        dataVal["nuevaFechaVencimiento"] = $("#id_nueva_fecha_vencimiento").val();

        $("#fondo_preloader").show();

        var forminput = JSON.stringify(dataVal);
        $.ajax(
            {
                    type : 'PUT',
                    url : ip_local + "/empenos/api_apartado/",
                    data : forminput,
                    contentType: "application/json; charset=utf-8",
                    datatype : "json",							
                     headers: {
                       'X-CSRFToken': csrf_token
                       },
                    success : function(data)
                    {	

                        console.log(data);

                        if (data.estatus == "0")
                        {
                            $("#encabezado_aviso").text("Error!!");
                            $("#msj_aviso").text(data.msj);
                            $(".cls_msj_aviso").show();
                        }
                        else
                        {
                            $("#encabezado_aviso").text("Exito!!");
                            $("#msj_aviso").text("Se reactivo correctamente.");
                            $(".cls_msj_aviso").show();
                        }

                        $("#fondo_preloader").hide();
                        
                    },
                    error : function(err)
                    {
                        $("#encabezado_aviso").text("Error!!");
                        $("#msj_error").text("Error al reactivar el apartado.");
                        $(".cls_msj_aviso").show();
                        $("#fondo_preloader").hide();
                    },
                    failure : function(f)
                    {
                        $("#encabezado_aviso").text("Error!!");
                        $("#msj_error").text("Error al cancelar la boleta");
                        $(".cls_msj_aviso").show();
                        $("#fondo_preloader").hide();
                    }
    
            }


        );
    }
}

function validaFormulario(){
    if($("#id_nueva_fecha_vencimiento").val() == ""){
        $(".cls_msj_aviso").show();
        $("#encabezado_aviso").text("Error!!");
        $("#msj_aviso").text("Debe indica la nueva fecha de vencimiento.");
        return false;
    }

    if($("#id_sucursal").val() == "" || $("#id_sucursal").val() == undefined ){
        $(".cls_msj_aviso").show();
        $("#encabezado_aviso").text("Error!!");
        $("#msj_aviso").text("Debe indicar una sucursal.");
        return false;
    }

    if($("#id_folio_boleta").val() == "" || $("#id_folio_boleta").val() == undefined){
        $(".cls_msj_aviso").show();
        $("#encabezado_aviso").text("Error!!");
        $("#msj_aviso").text("Debe indicar el folio de boleta.");
        return false;
    }


    if($("#id_folio_apartado").val() == "" || $("#id_folio_apartado").val() == undefined){
        $(".cls_msj_aviso").show();
        $("#encabezado_aviso").text("Error!!");
        $("#msj_aviso").text("Debe indicar el folio del apartado que desea reactivar.");
        return false;
    }
    return true;
}
