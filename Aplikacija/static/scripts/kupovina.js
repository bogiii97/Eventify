/**
 *Implementirao: Bogdan Radosavljevic, 2020/0109
 * Ovo je skripta koja se izvrsava kada se kupuje karta
 * */
$(document).ready(function (){
    if($("#proba").length>0){
        let tekst = $("#proba").text();
        let nizPodataka = tekst.split(" ");
        $("#id_ime").val(nizPodataka[0]);
        $("#id_prezime").val(nizPodataka[1]);
        $("#id_mejl").val(nizPodataka[2]);
    };

        $("#levo1").on('click',function(){
            let dogadjajId = $("#dogadjajId").data("dogid");
            //window.location.href = `/zavrsetak/${dogadjajId}/';
            window.location.href = `/`;
        });


    $("#desno1").on('click',function(){
        if(validirajFormu()) {
            resetujGreske();
            if ($("#preuzimanje").prop("checked")) {
                $("#desno2").text("Rezerviši ->");
                $("#pb2").text("50%");
                $("#pb2").css("width", "50%");
            } else {
                $("#desno2").text("Plaćanje ->");
                $("#pb2").text("33%");
                $("#pb2").css("width", "33%");
            }

            $("#kupacImePrezime").text("Ime i prezime: " + $("#id_ime").val() + " " + $("#id_prezime").val());
            $("#kupacDrzava").text("Država: " + $("#id_drzava").val());
            $("#kupacGrad").text("Grad: " + $("#id_grad").val());
            $("#kupacMejl").text("Mejl: " + $("#id_mejl").val());$("#kupacBrojTelefona").text("Broj telefona: " + $("#id_brojTelefona").val());

            $("#podaciOKupcu").addClass("d-none");
            $("#pregledNarudzbine").removeClass("d-none");
        }
    });


    $("#levo2").on('click',function(){
        $("#podaciOKupcu").removeClass("d-none");
        $("#pregledNarudzbine").addClass("d-none");
    });

    $("#desno2").on('click',function(){
        if($("#preuzimanje").prop("checked")){
            let dogadjajId = $("#dogadjajId").data("dogid");
            let status = "1";
            let tekst = dogadjajId + " " + status;
            for(let i = 0; i < ids.length; i++){
                tekst += " " + ids[i];
            }
            window.location.href = `/zavrsetak/${tekst}/`;
        }
        else {
            $("#pregledNarudzbine").addClass("d-none");
            $("#podaciSaKartice").removeClass("d-none");
        }
    });

    $("#levo3").on('click',function(){
        let dogadjajId = $("#dogadjajId").data("dogid");
        //window.location.href = `/zavrsetak/${dogadjajId}/';
        window.location.href = `/`;
    });

    $("#desno3").on('click',function(){
        if(validirajKarticu()){
            //TO DO back-end deo
            let dogadjajId = $("#dogadjajId").data("dogid");
            let status = "0";
            let tekst = dogadjajId + " " + status;
            for(let i = 0; i < ids.length; i++){
                tekst += " " + ids[i];
            }
            window.location.href = `/zavrsetak/${tekst}/`;
        }
    });



    $("#desno1").mouseenter(function() {
        if($("#preuzimanje").prop("checked")){
            $("#pb1").text("50%");
            $("#pb1").css("width", "50%");
        }
        else{
            $("#pb1").text("33%");
            $("#pb1").css("width", "33%");
        }
    });
    $("#desno1").mouseleave(function() {
        $("#pb1").css("width", "20px");
        $("#pb1").text("0%");
    });

    $("#levo2").mouseenter(function (){
        $("#pb2").text("0%");
        $("#pb2").css("width", "20px");
    })
    $("#levo2").mouseleave(function() {
        if($("#preuzimanje").prop("checked")){
            $("#pb2").text("50%");
            $("#pb2").css("width", "50%");
        }
        else {
            $("#pb2").text("33%");
            $("#pb2").css("width", "33%");
        }
    });

     $("#desno2").mouseenter(function (){
         if($("#preuzimanje").prop("checked")){
            $("#pb2").text("100%");
            $("#pb2").css("width", "100%");
         }
         else {
             $("#pb2").text("67%");
             $("#pb2").css("width", "67%");
         }
    })
    $("#desno2").mouseleave(function() {
        if($("#preuzimanje").prop("checked")){
            $("#pb2").text("50%");
            $("#pb2").css("width", "50%");
        }
        else {
            $("#pb2").text("33%");
            $("#pb2").css("width", "33%");
        }
    });

     $("#levo3").mouseenter(function (){
        $("#pb3").text("0%");
        $("#pb3").css("width", "20px");
    })
    $("#levo3").mouseleave(function() {
        $("#pb3").text("67%");
        $("#pb3").css("width", "67%");
    });
     $("#desno3").mouseenter(function (){
        $("#pb3").text("100%");
        $("#pb3").css("width", "100%");
    })
    $("#desno3").mouseleave(function() {
        $("#pb3").text("67%");
        $("#pb3").css("width", "67%");
    });

    $("#id_cvc").change(function (){
        if(!/^\d{3,4}$/.test(this.value)) {
            $("#id_cvc").css("border", "3px solid red")
        }
        else{
            $("#id_cvc").css("border", "");
        }
    })
    $("#id_vaziDo").change(function (){
        if(!/^(0[1-9]|1[0-2])\/([0-9]{2})$/.test(this.value)) {
            $("#id_vaziDo").css("border", "3px solid red")
        }
        else{
            $("#id_vaziDo").css("border", "");
        }
    })

    $("#id_brojKartice").change(function(){
        if(!/^\d{4}-\d{4}-\d{4}-\d{4}$/.test($("#id_brojKartice").val())){
            $("#id_brojKartice").css("border", "3px solid red")
        }
        else{
            $("#id_brojKartice").css("border", "");
        }
    })

});

function validirajKarticu(){
    let res = true;
    if(!/^\d{3,4}$/.test($("#id_cvc").val())){
        $("#id_cvc").css("border", "3px solid red")
        res = false;
    }
    if(!/^(0[1-9]|1[0-2])\/([0-9]{2})$/.test($("#id_vaziDo").val())) {
        $("#id_vaziDo").css("border", "3px solid red")
        res = false;
    }
    if(!/^\d{4}-\d{4}-\d{4}-\d{4}$/.test($("#id_brojKartice").val())){
        $("#id_brojKartice").css("border", "3px solid red")
        res = false;
    }

    return res;
}

function validirajFormu(){

    let res = true;
    if($("#id_ime").val() === ""){
        $("#imeLabela").css("padding-left", "126px");
        $("#imeGreska").text("Morate uneti ime");
        res = false;
    }
    else{
        $("#imeLabela").css("padding-right", "5px").css("padding-left", "0px");
        $("#imeGreska").text("");
    }
    if($("#id_prezime").val() === ""){
        $("#prezimeLabela").css("padding-left", "168px");
        $("#prezimeGreska").text("Morate uneti prezime");
        res = false;
    }
    else{
        $("#prezimeLabela").css("padding-right", "46px").css("padding-left", "12px");
        $("#prezimeGreska").text("");
    }
    if($("#id_mejl").val() === ""){
        $("#mejlLabela").css("padding-left", "142px");
        $("#mejlNevalidanGreska").text("");
        $("#mejlPrazanGreska").text("Morate uneti mejl");
        res = false;
    }
    else if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test($("#id_mejl").val())){
        $("#mejlLabela").css("padding-left", "225px");
        $("#mejlPrazanGreska").text("");
        $("#mejlNevalidanGreska").text("Mejl je u nevalidnom formatu");
        res = false;
    }
    else{
        $("#mejlLabela").css("padding-right", "85px").css("padding-left", "11px");
        $("#mejlPrazanGreska").text("");
        $("#mejlNevalidanGreska").text("");
    }


    return res;
}

//Za slucaj kad se vracamo sa prethodne stranice
function resetujGreske(){
    $("#imeLabela").css("padding-right", "5px").css("padding-left", "0px");
    $("#imeGreska").text("");
    $("#prezimeLabela").css("padding-right", "46px").css("padding-left", "12px");
    $("#prezimeGreska").text("");
    $("#mejlLabela").css("padding-right", "85px").css("padding-left", "11px");
    $("#mejlPrazanGreska").text("");
    $("#mejlNevalidanGreska").text("");
}