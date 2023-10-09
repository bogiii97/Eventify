/**
 *Implementirao: Vladan Vasic, 2020/0040
 * Ovo je skripta koja se izvrsava kada se udje na stranicu za objavljivanje dogadjaja
 * */
$(document).ready(function (){
    $('body').addClass('ostalo-pozadina');

    $('.nav-item').removeProp('disabled').removeProp('active');

    $("#prijavaDugme").addClass("d-none");
    $("#registracijaDugme").addClass("d-none");

    $("#odjavaDugme").removeClass("d-none");
    $("#novDogadjajDugme").removeClass("d-none").prop('disabled', true);

    $("#objavaForm").submit(function (event){
        event.preventDefault();

        if(validirajFormu()){
            this.submit();
        }
    });
    /**
     *Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja se izvrsava kada organizator zeli da doda novu vrstu karte
     * */
    $("#novaKartaDugme").click(function (){
        let karta = novaKarta();
        $("#karte").append(
          $(karta)
        );
    });
    /**
     *Implementirao: Vladan Vasic, 2020/0040
     * Ovo su funkcije koje se izvrsavaju kada korisnik bira tip dogadjaja koji zeli da organizuje
     * */
    $("#pozoristeRadio").click(function (){
        $('div.sport, div.zurka, div.muzika, div.ostalo').addClass('d-none');
        $('div.pozoriste').removeClass('d-none');
        $('body').removeClass('ostalo-pozadina').addClass('pozoriste-pozadina').removeClass('zurka-pozadina').removeClass('muzika-pozadina').removeClass('sport-pozadina');
    });
    $("#sportRadio").click(function (){
        $('div.pozoriste, div.zurka, div.muzika, div.ostalo').addClass('d-none');
        $('div.sport').removeClass('d-none');
        $('body').removeClass('ostalo-pozadina').removeClass('pozoriste-pozadina').removeClass('zurka-pozadina').removeClass('muzika-pozadina').addClass('sport-pozadina');
    });

    $("#muzikaRadio").click(function (){
        $('div.sport, div.zurka, div.pozoriste, div.ostalo').addClass('d-none');
        $('div.muzika').removeClass('d-none');
        $('body').removeClass('ostalo-pozadina').removeClass('pozoriste-pozadina').removeClass('sport-pozadina').removeClass('zurka-pozadina').addClass('muzika-pozadina');
    });

    $("#zurkaRadio").click(function (){
        $('div.sport, div.pozoriste, div.muzika, div.ostalo').addClass('d-none');
        $('div.zurka').removeClass('d-none');
        $('body').removeClass('ostalo-pozadina').removeClass('pozoriste-pozadina').removeClass('sport-pozadina').removeClass('muzika-pozadina').addClass('zurka-pozadina');
    });

    $("#ostaloRadio").click(function (){
        $('div.sport, div.zurka, div.muzika, div.pozoriste').addClass('d-none');
        $('div.ostalo').removeClass('d-none');
        $('body').addClass('ostalo-pozadina').removeClass('pozoriste-pozadina').removeClass('sport-pozadina').removeClass('muzika-pozadina').removeClass('zurka-pozadina');
    });

    $(".btn-close").click(function (){
        $("div.alert").addClass("d-none");
    });
});
/**
 *Implementirao: Vladan Vasic, 2020/0040
 * Ovo je funkcija koja pravi sadrzaj za jednu kartu koji se ubacuje na html stranicu
 * */
function novaKarta(){
    let karta = '<div class="col-4 p-2">' +
        '<label>Cena:</label>' +
        '<input type="number" name="cena" required>' +
        '</div>' +
        '<div class="col-4 p-2">' +
        '<label>Tip:</label>' +
        '<input type="text" name="tip" maxlength="50" required>' +
        '</div>' +
        '<div class="col-4 p-2">' +
        '<label>Broj karata:</label>' +
        '<input type="number" name="broj" required>' +
        '</div>';
    return karta;
}
/**
 *Implementirao: Vladan Vasic, 2020/0040
 * Ovo je funkcija koja se poziva kada korisnik klikne na dugme Objavi Dogadjaj da bi se proverila validnost forme
 * Ako forma nije validna, prikazuje se poruka u vidu JavaScript alert-a
 * */
function validirajFormu(){

    if($("#id_naziv").val() === ""){
        $(".alert-naziv").removeClass("d-none");
        return false;
    }
    if($("#id_adresa").val() === ""){
        $(".alert-adresa").removeClass("d-none");
        return false;
    }

    let trenutniDatum = new Date();
    let poslatiDatum = new Date($("#id_datum_vreme").val())

    if(trenutniDatum > poslatiDatum){
        $(".alert-datum").removeClass("d-none");
        return false;
    }
    if($("#id_kratak_opis").val() === ""){
        $(".alert-kratak-opis").removeClass("d-none");
        return false;
    }
    if($("#id_opis").val() === ""){
        $(".alert-opis").removeClass("d-none");
        return false;
    }
    let cene = document.querySelectorAll("input[name='cena']");
    let tip = document.querySelectorAll("input[name='tip']");
    let broj = document.querySelectorAll("input[name='broj']");
    if(cene.length == 0){
        $(".alert-nema-karata").removeClass("d-none");
        return false;
    }
    for(let i=0; i<cene.length; i++){
        if(cene[i].value === ""){
            $(".alert-nema-cene").removeClass("d-none");
            return false;
        }
        if(parseInt(cene[i].value) < 0){
            $(".alert-negativna-cena").removeClass("d-none");
            return false;
        }
    }
    for(let i=0; i<broj.length; i++){
        if(broj[i].value === ""){
            $(".alert-nema-broja").removeClass("d-none").show();
            return false;
        }
        if(parseInt(broj[i].value) < 0){
            $(".alert-negativan-broj").removeClass("d-none").show();
            return false;
        }
    }
    for(let i=0; i<tip.length; i++){
        if(tip[i].value === ""){
            $(".alert-nema-tipa").removeClass("d-none").show();
            return false;
        }
    }
    let vrsta_dogadjaja = $("input[type='radio']:checked").val();
    if(vrsta_dogadjaja === 'pozoriste'){
        if($('#id_zanr').val() === ''){
            $(".alert-nema-zanr").removeClass("d-none").show();
            return false;
        }
        if($('#id_glumci').val() === ''){
            $(".alert-nema-glumci").removeClass("d-none").show();
            return false;
        }
        if($('#id_trajanje').val() === ''){
            $(".alert-nema-trajanje").removeClass("d-none").show();
            return false;
        }
        if(/^\d{2}:\d{2}$/.test($('#id_trajanje').val()) == false){
            $(".alert-format-trajanje").removeClass("d-none").show();
            return false;
        }
    }
    else if(vrsta_dogadjaja === 'muzika'){
        if($('#id_izvodjac').val() === ''){
            $(".alert-izvodjac").removeClass("d-none").show();
            return false;
        }
    }
    else if(vrsta_dogadjaja === 'sport'){
        if($('#id_ucesnici').val() === ''){
            $(".alert-ucesnici").removeClass("d-none").show();
            return false;
        }
        if($('#id_naziv_sporta').val() === ''){
            $(".alert-naziv-sporta").removeClass("d-none").show();
            return false;
        }
    }
    else if(vrsta_dogadjaja === 'zurka'){
        if($('#id_izv').val() === ''){
            $(".alert-izvodjac").removeClass("d-none").show();
            return false;
        }
        if($('#id_vrsta_muzike').val() === ''){
            $(".alert-vrsta-muzike").removeClass("d-none").show();
            return false;
        }
    }
    if($("#id_slika").get(0).files.length === 0){
        $(".alert-slika").removeClass("d-none").show();
        return false;
    }
    return true;
}