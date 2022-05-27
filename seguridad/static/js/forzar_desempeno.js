 $(document).ready(
    function(){
        $(".cls_ayuda").hide();

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

        $(".cls_msj_aviso").hide();
        
        $("#btn_aceptar_aviso").click(
            function(){
                $(".cls_msj_aviso").hide();
            }
        );
        $("#btn_guardar").click(
            function(){
                forzarImporteDesempeno()
            }
        );
    }
);

function forzarImporteDesempeno(){
    if($("#id_sucursal").val() == "" || $("#id_sucursal").val() == undefined ){
        $(".cls_msj_aviso").show();
        $("#encabezado_aviso").text("Error!!");
        $("#msj_aviso").text("Debe indicar una sucursal.");
        return false;
    }

    if($("#id_folio").val() == "" || $("#id_folio").val() == undefined){
        $(".cls_msj_aviso").show();
        $("#encabezado_aviso").text("Error!!");
        $("#msj_aviso").text("Debe indicar un folio de boleta.");
        return false;
    }

    
    if($("#id_precio_desempeno").val() == "" || $("#id_precio_desempeno").val() == undefined || parseInt($("#id_precio_desempeno").val()) <= 0){
        $(".cls_msj_aviso").show();
        $("#encabezado_aviso").text("Error!!");
        $("#msj_aviso").text("El importe para desempeño debe ser mayor a cero.");
        return false;
    }

    put();
}

function inicio(token,un,ip){
    csrf_token = token;
	username = un;
	ip_local = ip;
}

function put(){
    var dat={};

    dat["folio_boleta"]= $("#id_folio").val();
    dat["id_sucursal"]= $("#id_sucursal").val();
    dat["nvo_importe"]= $("#id_precio_desempeno").val();


    $.ajax(
        {
                type : 'PUT',
                url : ip_local + "/empenos/api_forzar_desempeno/",
                data : JSON.stringify(dat),
                contentType: "application/json; charset=utf-8",
                datatype : "json",							
                 headers: {
                   'X-CSRFToken': csrf_token
                   },
                success : function(data)
                {	
                    console.log(data);
                    console.log(data["estatus"]);
                    console.log(data.estatus);

                    if (data.estatus == "0")
                    {
                        $("#encabezado_aviso").text("Error!!");
                        $("#msj_aviso").text(data.msj);
                        $(".cls_msj_aviso").show();
                    }
                    else
                    {
                        $("#encabezado_aviso").text("Exito!!");
                        $("#msj_aviso").text("Se actualizo correctamente.");
                        $(".cls_msj_aviso").show();
                    }

                    $("#fondo_preloader").hide();
                    
                },
                error : function(err)
                {
                    $("#encabezado_aviso").text("Error!!");
                    $("#msj_error").text("Error al actualizar la información.");
                    $(".cls_msj_aviso").show();
                    $("#fondo_preloader").hide();
                },
                failure : function(f)
                {
                    $("#encabezado_aviso").text("Error!!");
                    $("#msj_error").text("Error al actualizar la información.");
                    $(".cls_msj_aviso").show();
                    $("#fondo_preloader").hide();
                }

        }


    );

}