var csrf_token="";
var username="";
var ip_local="";

function inicio(token,un,ip){    
    csrf_token = token;
	username = un;
	ip_local = ip;
}


$(document).ready(
    function(){

        $("#fondo_preloader").hide();
        $(".cls_msj_aviso").hide();
        $(".cls_agregar_dia").hide();

        $("#btn_agregar_dia").click(
            function(){
                $(".cls_agregar_dia").hide();
                agregar_dia();
                $("#fecha_no_laboral").val("");
            }  
        );

        $("#btn_aceptar_aviso").click(
            function(){
                $(".cls_msj_aviso").hide();
            }
        );
        $("#btn_consultar_dias").click(
            function(){
                consulta_dias_no_laborales();
            }
        );

        $("#btn_mostrar_agregar_dia").click(
            function()
            {
                $(".cls_agregar_dia").show();
            }
        );
        $("#btn_cancelar_agregar_dia").click(
            function(){
                $(".cls_agregar_dia").hide();
                $("#fecha_no_laboral").val("");
            }
        );
    }
);


function validar_formulario(){
    let fecha = $("#fecha_no_laboral").val();

    if($("#fecha_no_laboral").val() == ""){
        $(".cls_msj_aviso").show();
        $("#encabezado_aviso").text("Error!!");
        $("#msj_aviso").text("Debe indicar la fecha que desea registrar como no laboral.");
        return false;
    }
    return true;


}

function agregar_dia(){
    if(validar_formulario())
    {
        var data = {};

        data["fecha"] = $("#fecha_no_laboral").val() ;

        data = JSON.stringify(data);

        $("#fondo_preloader").show();

        $.ajax(
            {
                    type : 'POST',
                    url : ip_local + "/empenos/api_dia_no_laboral/",
                    data : data,
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
                            $("#msj_aviso").text("El día se agrego correctamente.");
                            $(".cls_msj_aviso").show();
                        }

                        $("#fondo_preloader").hide();
                        
                    },
                    error : function(err)
                    {
                        $("#encabezado_aviso").text("Error!!");
                        $("#msj_error").text("Error al agrear el dia no laboral.");
                        $(".cls_msj_aviso").show();
                        $("#fondo_preloader").hide();
                    },
                    failure : function(f)
                    {
                        $("#encabezado_aviso").text("Error!!");
                        $("#msj_error").text("Error al agrear el dia no laboral");
                        $(".cls_msj_aviso").show();
                        $("#fondo_preloader").hide();
                    }
    
            }


        );
    }
}

function consulta_dias_no_laborales()
{
    year=$("#year").val();
    $("#tabla_dias_no_laborales tbody tr").remove();
    $("#fondo_preloader").show();
    $.ajax({
        type: "GET",
        url:  ip_local + "/empenos/api_dia_no_laboral?year="+year/*,
        data: {

            "id_cliente":id_cliente

        }*/,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (r) 
        {
            console.log(r);
            fn_agregarFila(r);
            $("#fondo_preloader").hide();

        },
        error: function (r) 
        {

                $("#msj_error").text("Error al consultar la información");
                $(".cls_msj_error").show();
                $("#fondo_preloader").hide();

        },
        failure: function (r) 
        {

                $("#msj_error").text("Error al consultar la información");
                $(".cls_msj_error").show();
                $("#fondo_preloader").hide();

        }
    });

}


function fn_agregarFila(obj) {
    var cont=obj.length;
    for(x=0; x<cont;x++)
    {
        var htmlTags = '<tr>'+

        "<td><a onClick='eliminar_dia("+obj[x].id.toString()+")' class='btn btn-default btn-sm'><span class='glyphicon glyphicon-remove'></span></a></td>"+
        '<td>' + obj[x].fecha.substring(0 ,10) + '</td>'+
        '</tr>';


        $('#tabla_dias_no_laborales tbody').append(htmlTags);
    }

}

function eliminar_dia(id){
    var data = {};

    data["iddia"] = id;

    data = JSON.stringify(data);

    $("#fondo_preloader").show();

    $.ajax(
        {
                type : 'DELETE',
                url : ip_local + "/empenos/api_dia_no_laboral/",
                data : data,
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
                        $("#fondo_preloader").hide();
                        return 0;
                    }

                    consulta_dias_no_laborales();                    
                    
                },
                error : function(err)
                {
                    $("#encabezado_aviso").text("Error!!");
                    $("#msj_error").text("Error al agrear el dia no laboral.");
                    $(".cls_msj_aviso").show();
                    $("#fondo_preloader").hide();
                },
                failure : function(f)
                {
                    $("#encabezado_aviso").text("Error!!");
                    $("#msj_error").text("Error al agrear el dia no laboral");
                    $(".cls_msj_aviso").show();
                    $("#fondo_preloader").hide();
                }

        }


    );
}