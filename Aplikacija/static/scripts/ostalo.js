/**
 *Implementirao: Vladan Vasic, 2020/0040
 * Ovo je skripta koja se izvrsava kada se udje na stranicu sa ostalim dogadjajima
 * */
$(document).ready(function () {
    $('.nav-link').removeClass('active');
    $('#ostaloLink').addClass('active');
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
        const grad = $("#grad").val();
        if (jedno_postavljeno()) {
            saljiZahtev(nazivVrednost, date_range, grad);
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
        const naziv = $("#naziv").val();
        const grad = $("#grad").val();
        saljiZahtev(naziv, date_range, grad);
    });
    /**
     *Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja se izvrsava kada se promeni vrednost polja za pretragu Grad
     * Tada se salje asinhroni POST request ka url-u pozoriste_pretraga koji vraca odgovarajuce dogadjaje koji prolaze filter
     * */
    $('#grad').on('keyup', (e) => {
        const nazivVrednost = $("#naziv").val();
        const date_range = $("input[name='daterange']").val();
        const grad = e.target.value;
        if (jedno_postavljeno()) {
            saljiZahtev(nazivVrednost, date_range, grad);
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
    let trenutniDatum = new Date();
    const grad = $("#grad").val();
    let dan = trenutniDatum.getDate();
    let mesec = trenutniDatum.getMonth() + 1;
    let godina = trenutniDatum.getFullYear();
    let def = mesec.toString().padStart(2, '0') + '/' + dan.toString().padStart(2, '0') + '/' + godina + ' - ' + mesec.toString().padStart(2, '0') + '/' + dan.toString().padStart(2, '0') + '/' + godina;

    return $('input[name="daterange"]').val() !== def || nazivVrednost !== '' || grad !== '';
}
/**
     * Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja dogadjaje koje je dobila na osnovu filtera iz backend dela ugradjuje u html stranicu
     * */
function dodajSadrzaj(data){
    data.forEach(item => {
                        let datum = item.datum_vreme.slice(0,10);
                        let vreme = item.datum_vreme.slice(11,19);
                        $('.sa-pretragom').append($(`<div class="row m-2 rounded border event-info">
                             <div class="col-sm-2 p-0 text-start">
                                <img class="img-fluid event-image rounded-1" src='/media/${item.slika}'>
                                    </div>
                                <div class="col-sm-10 event-text"> 
                                    <h4>${item.naziv}</h4>
                                    <p class="mb-1">${item.kratak_opis}</p>
                                    <hr class="m-0 p-0">
                                    <p class="mb-1"><strong>Vreme: </strong>${datum} ${vreme}</p>
                                    <a href="/dogadjaj/${item.id}" class="btn btn-light">Više detalja</a>
                                </div>`));
                    });
}
/**
     *Implementirao: Vladan Vasic, 2020/0040
     * Ovo je funkcija koja salje asinhromo POST request backend strani
     * */
function saljiZahtev(naziv, date_range, grad){
    fetch('/ostalo_pretraga/', {
                body: JSON.stringify({
                    naziv: naziv,
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