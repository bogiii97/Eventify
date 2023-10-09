/**
 *Implementirao: Mateja Milenkovic, 2020/0514
 * Ovo je skripta koja se izvrsava prilikom login-a
 * */

$(document).ready(function (){
    $("#prijavaDugme").addClass("d-none");
    $("#registracijaDugme").addClass("d-none");
    $("#odjavaDugme").addClass("d-none");

    $("#korisnicko_ime_id").css("margin-right", "82px");
    $("#sifra_id").css("margin-left", "52px");



    /**
     *Implementirao: Mateja Milenkovic, 2020/0514
     * Ovo je funkcija kada korisnik pritisne dugme "Prijavi se". Tada se pre submitovanja forme vrsi validacija svih polja forme i ukoliko
     * ima gresaka, izaći će poruka o napravljenoj grešci, u suprotnom će se korisnik ulogovati na platformu.
     * */
    $('#login-form').on('submit', function (event) {
        event.preventDefault();

        $('#korisnicko-ime-error').text('');
        $('#sifra-error').text('');

        let username = $('#id_username').val();
        let password = $('#id_password').val();

        let errors = false;

        if (username === '') {
            $('#korisnicko-ime-error').text('Unesite korisničko ime!');
            errors = true;
        }

        if (password === '') {
            $('#sifra-error').text('Unesite šifru!');
            errors = true;
        }

        if (errors == false) {
            $('#login-form')[0].submit();
        }
    });

});