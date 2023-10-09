/**
 *Implementirao: Mateja Milenkovic, 2020/0514
 * Ovo je skripta koja se izvrsava prilikom registracije, vrši se provera unetih polja,
 * ispisuje poruka o grešci ako ona postoji, u suprotnom se submituje forma i korisnik/organizator
 * šalje ulogovan na početnu stranicu platforme
 * */
$(document).ready(function (){
    $("#prijavaDugme").addClass("d-none");
    $("#registracijaDugme").addClass("d-none");
    $("#odjavaDugme").addClass("d-none");

    $("#gradLabela").css("margin-right", "0px");
    $("#gradLabela").css("width", "335px");

    $("#slikaLabela").css("margin-left", "85px");


    var usernameInput = document.getElementById("id_username");
    usernameInput.oninvalid = function () {

        if (this.value === '') this.setCustomValidity('Unesite korisničko ime!');

    };
    usernameInput.oninput = function () {
        this.setCustomValidity("");
    };

    var emailInput = document.getElementById("id_email");
    emailInput.oninvalid = function() {
        if (this.value === '') {
            this.setCustomValidity("Unesite vašu e-poštu.");
        } else {
            this.setCustomValidity("Unesite validnu e-poštu.");
        }
    };
    emailInput.oninput = function() {
        this.setCustomValidity("");
    };

    var imeInput = document.getElementById("id_ime");
    imeInput.oninvalid = function () {

        if (this.value === '') this.setCustomValidity('Unesite ime!');


    };
    imeInput.oninput = function () {
        this.setCustomValidity("");
    };

    var prezimeInput = document.getElementById("id_prezime");
    prezimeInput.oninvalid = function () {

        if (this.value === '') this.setCustomValidity('Unesite prezime!');


    };
    prezimeInput.oninput = function () {
        this.setCustomValidity("");
    };


    var password1Input = document.getElementById("id_password1");
    password1Input.oninvalid = function () {
        if (this.value === '') {
            this.setCustomValidity("Unesite šifru!");
        } else {
            this.setCustomValidity("Ne poklapaju se šifre!.");
        }
    };
    password1Input.oninput = function () {
        this.setCustomValidity("");
    };

    var password2Input = document.getElementById("id_password2");
    password2Input.oninvalid = function () {
        if (this.value === '') {
            this.setCustomValidity("Unesite potvrdu šifre!");
        } else {
            this.setCustomValidity("Ne poklapaju se šifre!.");
        }
    };
    password2Input.oninput = function () {
        this.setCustomValidity("");
    };

});
