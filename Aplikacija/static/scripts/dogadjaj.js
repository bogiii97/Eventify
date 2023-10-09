/**
 *Implementirao: Bogdan Radosavljevic, 2020/0109
 * Ovo je skripta koja se izvrsava kada se udje za pregled jednog događaja
 * */
$(document).ready(function (){
    for(let i = 0; i < preostaloOdSvakogTipa.length; i++){
        $("#" + preostaloOdSvakogTipa[i]).text(tipovi[i] + "-");
    }

    for(let i = 0; i < tipovi.length; i++){
        $("#" + tipovi[i]).val(0);
        $("#" + tipovi[i]).on('input',function(){
            let val = this.value;
            if(!/^[0-9]*$/.test(val)) {this.value = val.substring(0, val.length - 1); return;}
            let ukCena = 0;
            for(let i = 0; i < tipovi.length; i++){
                if($("#" + tipovi[i]).val() == "") continue;
                ukCena += parseInt($("#" + tipovi[i]).val()) * cene[i];
            }
            $("#ukCena").text(ukCena);

        })
    }


    $("#kupi").on('click', function(){
        if(validirajKarte()){
            let tekst = dogadjaj_id + " " + $("#ukCena").text();
            for(let i = 0; i < tipovi.length; i++){
                if(parseInt($("#" + tipovi[i]).val()) != 0){
                    tekst += " " + tipovi[i];
                    tekst += " " + $("#" + tipovi[i]).val();
                }
            }
            $("#neMozeKupi").text("")
            $("#kupiLabel").css("padding-right", "0px")
            window.location.href = `/kupovina/${tekst}/`;
        }
    })
});

function validirajKarte(){
    let nisuSveNule = false;
    for(let i = 0; i < tipovi.length; i++){
        if(parseInt($("#" + tipovi[i]).val()) != 0 && $("#" + tipovi[i]).val() != ""){
            nisuSveNule = true;
            break;
        }
    }
    if(!nisuSveNule) {
        $("#neMozeKupi").text("Morate kupiti bar 1 kartu")
        //$("#kupiLabel").css("padding-right", "180px")
        return false;
    }

    let imaDovoljno = true;
    for(let i = 0; i < tipovi.length; i++){
        if(parseInt($("#" + tipovi[i]).val()) > parseInt(preostaloOdSvakogTipa[i])){
            imaDovoljno = false;
            break;
        }
    }
    if(!imaDovoljno){
        $("#neMozeKupi").text("Nema dovoljno karata")
        //$("#kupiLabel").css("padding-right", "160px")
        return false;
    }

    return true;
}