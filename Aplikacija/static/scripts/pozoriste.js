/**
 *Implementirao: Vladan Vasic, 2020/0040
 * Ovo je skripta koja se izvrsava kada se udje na stranicu sa pozorisnim dogadjajima
 * */

$(document).ready(function () {
    $('.nav-link').removeClass('active');
    $('#pozoristeLink').addClass('active');
    let trenutniDatum = new Date();
    let dan = trenutniDatum.getDate();
    let mesec = trenutniDatum.getUTCMonth() + 1;
    let godina = trenutniDatum.getUTCFullYear();
    let def = mesec.toString().padStart(2, '0') + '/' + dan.toString().padStart(2, '0') + '/' + godina + ' - ' + mesec.toString().padStart(2, '0') + '/' + dan.toString().padStart(2, '0') + '/' + godina;
    $("input[name='daterange']").val(def);
    $(function () {
        $('input[name="daterange"]').daterangepicker({
            opens: 'left'
        }, function (start, end, label) {

        });
    });
    /**
     *Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja se izvrsava kada se promeni vrednost polja za pretragu Naziv
     * Tada se salje asinhroni POST request ka url-u pozoriste_pretraga koji vraca odgovarajuce dogadjaje koji prolaze filter
     * */
    $('#naziv').on('keyup', (e) => {
        const nazivVrednost = e.target.value;
        const date_range = $("input[name='daterange']").val();
        const zanr = $("#zanr").val();
        const glumci = $("#glumci").val();
        const grad = $("#grad").val();

        if (jedno_postavljeno()) {
            saljiZahtev(nazivVrednost, zanr, glumci, date_range, grad);
        } else {

            $('.bez-pretrage').removeClass('d-none');
            $('.sa-pretragom').addClass('d-none').html('');
        }
    });
    /**
     *Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja se izvrsava kada se promeni opseg datuma
     * Tada se salje asinhroni POST request ka url-u pozoriste_pretraga koji vraca odgovarajuce dogadjaje koji prolaze filter
     * */
    $('input[name="daterange"]').on('change', (e) => {
        const date_range = e.target.value;
        const nazivVrednost = $('#naziv').val();
        const zanr = $("#zanr").val();
        const glumci = $("#glumci").val();
        const grad = $("#grad").val();
        saljiZahtev(nazivVrednost, zanr, glumci, date_range, grad);
    });
    /**
     *Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja se izvrsava kada se promeni vrednost polja za pretragu Zanr
     * Tada se salje asinhroni POST request ka url-u pozoriste_pretraga koji vraca odgovarajuce dogadjaje koji prolaze filter
     * */
    $('#zanr').on('keyup', (e) => {
        const nazivVrednost = $('#naziv').val();
        const date_range = $("input[name='daterange']").val();
        const zanr = e.target.value;
        const glumci = $("#glumci").val();
        const grad = $("#grad").val();
        if (jedno_postavljeno()) {
            saljiZahtev(nazivVrednost, zanr, glumci, date_range, grad);
        } else {
            $('.bez-pretrage').removeClass('d-none');
            $('.sa-pretragom').addClass('d-none').html('');
        }
    });
    /**
     *Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja se izvrsava kada se promeni vrednost polja za pretragu Glumci
     * Tada se salje asinhroni POST request ka url-u pozoriste_pretraga koji vraca odgovarajuce dogadjaje koji prolaze filter
     * */
    $('#glumci').on('keyup', (e) => {
        const nazivVrednost = $('#naziv').val();
        const date_range = $("input[name='daterange']").val();
        const zanr = $("#zanr").val();
        const glumci = e.target.value;
        const grad = $("#grad").val();
        if (jedno_postavljeno()) {
            saljiZahtev(nazivVrednost, zanr, glumci, date_range, grad);
        } else {
            $('.bez-pretrage').removeClass('d-none');
            $('.sa-pretragom').addClass('d-none').html('');
        }
    });
    /**
     *Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja se izvrsava kada se promeni vrednost polja za pretragu Grad
     * Tada se salje asinhroni POST request ka url-u pozoriste_pretraga koji vraca odgovarajuce dogadjaje koji prolaze filter
     * */
    $('#grad').on('keyup', (e) => {
        const nazivVrednost = $('#naziv').val();
        const date_range = $("input[name='daterange']").val();
        const zanr = $("#zanr").val();
        const glumci = $("#glumci").val();
        const grad = e.target.value;
        if (jedno_postavljeno()) {
            saljiZahtev(nazivVrednost, zanr, glumci, date_range, grad);
        } else {
            $('.bez-pretrage').removeClass('d-none');
            $('.sa-pretragom').addClass('d-none').html('');
        }
    });
});
/**
     *Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja ukazuje da li je bar jedno polje za pretragu postavljeno
 */
function jedno_postavljeno() {
    const nazivVrednost = $("#naziv").val();
    const zanr = $("#zanr").val();
    const glumci = $("#glumci").val();
    const grad = $("#grad").val();
    let trenutniDatum = new Date();
    let dan = trenutniDatum.getDate();
    let mesec = trenutniDatum.getMonth() + 1;
    let godina = trenutniDatum.getFullYear();
    let def = mesec.toString().padStart(2, '0') + '/' + dan.toString().padStart(2, '0') + '/' + godina + ' - ' + mesec.toString().padStart(2, '0') + '/' + dan.toString().padStart(2, '0') + '/' + godina;

    return $('input[name="daterange"]').val() !== def || nazivVrednost !== '' || zanr !== '' || glumci !== '' || grad !== '';
}
/**
     * Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja dogadjaje koje je dobila na osnovu filtera iz backend dela ugradjuje u html stranicu
     * */
function dodajSadrzaj(data){
    console.log(data);
    data.forEach(item => {
                        let datum = item.datum_vreme.slice(0,10);
                        let vreme = item.datum_vreme.slice(11,19);
                        let trajanje = item.trajanje;
                        let sati = trajanje.slice(5, 6);
                        let minuti = trajanje.slice(7, 9);
                        let sekunde = trajanje.slice(10, 12);
                        let period = sati + ':' + minuti + ':' + sekunde;
                        $('.sa-pretragom').append($(`<div class="row m-2 rounded border event-info">
                             <div class="col-sm-2 p-0 text-start">
                                <img class="img-fluid event-image rounded-1" src='/media/${item.slika}'>
                                    </div>
                                <div class="col-sm-10 event-text"> 
                                    <h4>${item.naziv}</h4>
                                    <p class="mb-1">${item.kratak_opis}</p>
                                    <hr class="m-0 p-0">
                                    <p class="mb-1"><strong>Vreme: </strong>${datum} ${vreme}</p>
                                    <p class="mb-1"><strong>Žanr: </strong>${item.zanr}</p>
                                    <p class="mb-1"><strong>Glumci: </strong>${item.glumci}</p>
                                    <p class="mb-1"><strong>Trajanje: </strong>${period}</p>
                                    
                                    <a href="/dogadjaj/${item.id}" class="btn btn-light">Više detalja</a>
                                </div>`));
                    });
}
/**
     *Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja salje asinhromo POST request backend strani
     * */
function saljiZahtev(naziv, zanr, glumci, date_range, grad){
    fetch('/pozoriste_pretraga/', {
                body: JSON.stringify({
                    naziv: naziv,
                    zanr: zanr,
                    glumci: glumci,
                    date_range: date_range,
                    grad: grad,
                }),
                method: 'POST',
            })
                .then((res) => res.json())
                .then((data) => {

                    $('.bez-pretrage').addClass('d-none');
                    $('.sa-pretragom').removeClass('d-none').html('');
                    dodajSadrzaj(data);

                })
}