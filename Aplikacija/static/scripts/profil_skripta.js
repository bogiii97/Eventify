/**
 *Implementirao: Marko Lukesevic, 2020/0246
 * Ovo je skripta koja se izvrsava kada se udje na stranicu profila
 * */

$(document).ready(function(){

    /**
     *Implementirao: Marko Lukesevic, 2020/0246
     * Ovo su funkcije koje se izvrsavaju kada korisnik u panelu bira sta zeli da prikaze (posecene dogadjaje, njegove recenzije ili organizovane dogadjaje ukoliko ih ima)
     * */
    $("#poseceni_dugme").on('click', function(){
        $(this).addClass("aktivirano");
        $("#organizovani_dugme").removeClass("aktivirano");
        $("#recenzije_dugme").removeClass("aktivirano");
        $("#poseceni_dogadjaji").removeClass("d-none");
        $("#organizovani_dogadjaji").addClass("d-none");
        $("#moje_recenzije").addClass("d-none");
    });

    $("#organizovani_dugme").on('click', function(){
        $(this).addClass("aktivirano");
        $("#poseceni_dugme").removeClass("aktivirano");
        $("#recenzije_dugme").removeClass("aktivirano");
        $("#organizovani_dogadjaji").removeClass("d-none");
        $("#poseceni_dogadjaji").addClass("d-none");
        $("#moje_recenzije").addClass("d-none");
    });

    $("#recenzije_dugme").on('click', function(){
        $(this).addClass("aktivirano");
        $("#poseceni_dugme").removeClass("aktivirano");
        $("#organizovani_dugme").removeClass("aktivirano");
        $("#poseceni_dogadjaji").addClass("d-none");
        $("#organizovani_dogadjaji").addClass("d-none");
        $("#moje_recenzije").removeClass("d-none");
    });

    /**
     *Implementirao: Marko Lukesevic, 2020/0246
     * Ovo je funkcija kada korisnik pritisne dugme "azuriraj profil". Tada se pre submitovanja forme vrsi validacija svih polja forme i salje se asinhroni
     * POST request na url provera-emaila koji vraca informaciju o tome da li u sistemu vec postoji korisnik sa zadatim e-mailom.
     * */
    $("#azuriraj-forma").on('submit', function(event){
        event.preventDefault();
       let email = $("#email").val();
       let lozinka = $("#lozinka").val();
       let email_postoji = false;
       let sifra_format = false;
       let email_format = false;
       let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
       $("#error-email").addClass("d-none").text("");
       $("#error-lozinka").addClass("d-none").text("");
       $.ajax({
           url: '/profil/azuriranje_profila/provera_emaila',
           method: 'POST',
           data: {
               csrfmiddlewaretoken: csrfToken,
               email: email
           },
           dataType: 'json',
           success: function(response){
               if (response.postoji_email){
                    email_postoji = true;
                    $("#error-email").removeClass("d-none").text("Vec postoji korisnik sa tim emailom");
               } else{
                   $("#error-email").addClass("d-none").text("");
               }

               //Ako postoji email i nije u dobrom formatu baci error
               if(email !== '' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){
                   email_format = true;
                   $("#error-email").removeClass("d-none").text("E-mail nije u dobrom formatu");
               };

               //Ako postoji password i nije u dobrom formatu baci error
                if(lozinka !== "" && (/^\d+$/.test(lozinka) || lozinka.length < 8)){
                    sifra_format = true;
                    $("#error-lozinka").removeClass("d-none").text("Sifra mora imati minimalno 8 karaktera i minimalno jedan znak koji nije cifra");
                }


               if(email_postoji === false && sifra_format === false && email_format === false){
                $("#azuriraj-forma")[0].submit();
               }

           },
           error: function(xhr, textStatus, errorThrown){

           }
       });



    });

});

/**
     *Implementirao: Marko Lukesevic, 2020/0246
     * Ovo je funkcija koja sluzi da prebaci korisnika na neki drugi url
     * */
function prebaciNaUrl(url){
    window.location.href = url;
}