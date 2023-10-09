import datetime

from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseForbidden
from django.http import JsonResponse
from urllib.parse import unquote
from django.http import Http404, HttpResponse
from .forms import *
import json
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
@login_required(login_url='login')
@permission_required('Aplikacija.add_dogadjaj')
def objava_dogadjaja(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return HttpResponse
            Implementirao Vladan Vasic, 2020/0040
            Ovo je backend deo za stranicu objava_dogadjaja koju organizator pokrece kada hoce da kreira dogadjdj
    '''
    dogadjajForm = DogadjajForm(data=request.POST or None)
    context = {
        'form': dogadjajForm
    }
    return render(request, template_name='templates/objava_dogadjaja.html', context=context)


@login_required(login_url='login')
@permission_required('Aplikacija.add_dogadjaj')
def kreiranje_dogadjaja(request: HttpRequest):
    '''
        @param request: HttpRequest
        @return HttpResponse
        Implementirao Vladan Vasic, 2020/0040
        Ovo url koji se izvrsava na backend strani kada organizator klikne dugme za kreiranje dogadjaja nakon unetih podataka
    '''
    dogadjajForm = DogadjajForm(request.POST, request.FILES)

    if dogadjajForm.is_valid():
        tip = request.POST.get('tipDogadjaja')
        if tip == 'pozoriste':
            dogadjaj = Pozoriste()
            dogadjaj.zanr = request.POST.get('zanr')
            dogadjaj.glumci = request.POST.get('glumci')
            sati, minuti = request.POST.get('trajanje').split(':')
            sati = int(sati)
            minuti = int(minuti)
            dogadjaj.trajanje = datetime.timedelta(hours=sati, minutes=minuti)
        elif tip == 'muzika':
            dogadjaj = Muzika()
            dogadjaj.izvodjac = request.POST.get('izvodjac')
        elif tip == 'sport':
            dogadjaj = Sport()
            dogadjaj.ucesnici = request.POST.get('ucesnici')
            dogadjaj.naziv_sporta = request.POST.get('naziv_sporta')
        elif tip == 'zurka':
            dogadjaj = Zurka()
            dogadjaj.vrsta_muzike = request.POST.get('vrsta_muzike')
            dogadjaj.izvodjac = request.POST.get('izvodjac_zurka')
        else:
            dogadjaj = Ostalo()
        dogadjaj.naziv = dogadjajForm.cleaned_data['naziv']
        dogadjaj.grad = Grad.objects.get(pk=int(dogadjajForm.cleaned_data['grad']))
        dogadjaj.adresa = dogadjajForm.cleaned_data['adresa']
        dogadjaj.datum_vreme = dogadjajForm.cleaned_data['datum_vreme']
        dogadjaj.kratak_opis = dogadjajForm.cleaned_data['kratak_opis']
        dogadjaj.opis = dogadjajForm.cleaned_data['opis']
        dogadjaj.slika = dogadjajForm.cleaned_data['slika']
        dogadjaj.organizator = request.user
        dogadjaj.save()
        for prod_id in dogadjajForm.cleaned_data['prodajno_mesto']:
            prodajno_mesto = ProdajnoMesto.objects.get(pk=int(prod_id))
            dogadjaj.prodaje_se.add(prodajno_mesto)
            dogadjaj.save()
        dogadjaj.save()

        for index in range(len(request.POST.getlist('cena'))):
            cena = int(request.POST.getlist('cena')[index])
            tip = request.POST.getlist('tip')[index]
            broj = int(request.POST.getlist('broj')[index])
            for i in range(broj):
                karta = Karta()
                karta.cena = cena
                karta.tip = tip
                karta.dogadjaj = dogadjaj
                karta.save()

    return redirect('pocetna')

def login_req(request: HttpRequest):
    '''
        @param request: HttpRequest
        @return HttpResponse
        Implementirao Mateja Milenkovic, 2020/0514
        Ovo je url koji se izvrsava na backend strani kada korisnik pozeli da se uloguje
    '''

    form = AuthenticationForm(request=request, data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('pocetna')  # redirect vraca na stranicu sa poljem name iz url
    context = {
        'form': form,
    }

    return render(request, 'templates/login.html', context)


def logout_req(request: HttpRequest):

    '''
        @param request: HttpRequest
        @return HttpResponse
        Implementirao Mateja Milenkovic, 2020/0514
        Ovo je url koji se izvrsava na backend strani kada korisnik pozeli da se izloguje
    '''

    logout(request)
    return redirect('pocetna')


def registration(request: HttpRequest):


    '''
        @param request: HttpRequest
        @return HttpResponse
        Implementirao Mateja Milenkovic, 2020/0514
        Ovo je url koji se izvrsava na backend strani kada korisnik pozeli da se registruje
    '''

    if request.method == 'POST':
        form = KorisnikCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Dodela grupe u zavisnosti od izabranog tipa korisnika
            tip_korisnika = request.POST.get('izborTipaKorisnika')
            if tip_korisnika == 'organizator':
                organizator_group = Group.objects.get(name='organizator')
                user.groups.add(organizator_group)
            else:
                korisnik_group = Group.objects.get(name='korisnik')
                user.groups.add(korisnik_group)


            login(request, user)
            return redirect('pocetna')
    else:
        form = KorisnikCreationForm()

    context = {'form': form }
    return render(request, 'templates/registracija.html', context)


def postavi_upit(request: HttpRequest):


    '''
        @param request: HttpRequest
        @return HttpResponse
        Implementirao Mateja Milenkovic, 2020/0514
        Ovo je url koji se izvrsava na backend strani kada korisnik pozeli da se posalje pitanje korisnickoj podrsci
    '''

    forma = UpitForma()

    if request.method == 'POST':
        forma = UpitForma(request.POST)
        if forma.is_valid():
            forma.save()
            return redirect('pocetna')

    context = {
        'form': forma
    }

    return render(request, 'templates/postavi_upit.html', context)

def kupovina(request: HttpRequest, tekst: str):
    '''
                    @param request: HttpRequest
                    @return HttpResponse
                    Implementirao Bogdan Radosavljevic, 2020/0109
                    Ovo je backend deo koji obradjuje proces kupovine karte
    '''
    try:
        niz = tekst.split(" ")
        dogadjaj_id = int(niz[0])
        cena = int(niz[1])
        tipovi = []
        kolicina = []
        ids = []
        tipKolicina = ""
        for i in range(2,len(niz),2):
            tipKolicina += niz[i] + "-" + niz[i+1] + " "
            tipovi.append(niz[i])
            kolicina.append(niz[i + 1])
        karte = []
        for i in range(len(tipovi)):
            karte = Karta.objects.filter(dogadjaj_id=dogadjaj_id, tip=tipovi[i], status='slobodna')
            for j in range(int(kolicina[i])):
                ids.append(karte[j].id)

        ima = False
        prodajnaMesta = ProdajnoMesto.objects.filter(dogadjaj__id=dogadjaj_id)
        if len(prodajnaMesta) > 0:
            ima = True

        dogadjaj = Dogadjaj.objects.get(pk=dogadjaj_id)
        form = kupacInfoForm(data=request.POST or None)
        formKartica = karticaInfoForm(data=request.POST or None)
        context = {
            'imaProdajna': ima,
            'cena': cena,
            'tipKolicina': tipKolicina,
            'dogId': dogadjaj_id,
            'dogNaziv': dogadjaj.naziv,
            'dogGrad': dogadjaj.grad.naziv,
            'dogAdresa': dogadjaj.adresa,
            'dogDatumVreme': dogadjaj.datum_vreme,
            'form': form,
            'formK': formKartica,
            'ids': json.dumps(ids)
        }
        return render(request, template_name='templates/kupovina.html', context=context)
    except Dogadjaj.DoesNotExist:
        raise Http404("Događaj not found")

def zavrsetak(request: HttpRequest, tekst: str):
    '''
                        @param request: HttpRequest
                        @return HttpResponse
                        Implementirao Bogdan Radosavljevic, 2020/0109
                        Ovo je backend deo koji proces nakon kupovine tj. ažuriranje u bazi
    '''
    niz = tekst.split(" ")
    for i in range(2, len(niz)):
        karta = Karta.objects.get(pk=niz[i])
        if(int(niz[1]) == 0):
            karta.status = "kupljena"
        else:
            karta.status = "rezervisana"
        if request.user.is_authenticated:
            karta.korisnik = request.user
        karta.save()
    context = {
        'dogId': niz[0],
        'status': niz[1]
    }
    return render(request, template_name='templates/zavrsetakKupovine.html', context=context)

def dogadjaj(request: HttpRequest, dogadjaj_id: int):
    '''
                        @param request: HttpRequest
                        @return HttpResponse
                        Implementirao Bogdan Radosavljevic 2020/0109, Vladan Vasic 2020/0040
                        Ovo je backend deo za pregled izabranog događaja
    '''
    if Sport.objects.filter(pk=dogadjaj_id).exists():
        dogadjaj = Sport.objects.get(pk=dogadjaj_id)
    elif Pozoriste.objects.filter(pk=dogadjaj_id).exists():
        dogadjaj = Pozoriste.objects.get(pk=dogadjaj_id)
    elif Muzika.objects.filter(pk=dogadjaj_id).exists():
        dogadjaj = Muzika.objects.get(pk=dogadjaj_id)
    elif Zurka.objects.filter(pk=dogadjaj_id).exists():
        dogadjaj = Zurka.objects.get(pk=dogadjaj_id)
    else:
        dogadjaj = Ostalo.objects.get(pk=dogadjaj_id)
    organizator_id = dogadjaj.organizator.id

    ima = False
    prodajnaMesta = ProdajnoMesto.objects.filter(dogadjaj__id=dogadjaj_id)
    if len(prodajnaMesta) > 0:
        ima = True

    context = {
        'imaProdajna': ima,
        'dogadjaj': dogadjaj
    }
    karte = []
    tipovi = []
    cene = []
    preostaloOdSvakogTipa = []
    for karta in Karta.objects.filter(dogadjaj_id=dogadjaj_id):
        if karta.tip not in tipovi:
            karte.append(karta)
            tipovi.append(unquote(karta.tip))
            cene.append(karta.cena)
    for tip in tipovi:
        objektiTipa = Karta.objects.filter(dogadjaj_id=dogadjaj_id, tip=tip, status='slobodna')
        preostaloOdSvakogTipa.append(len(objektiTipa))

    context['karte'] = karte
    context['tipovi'] = json.dumps(tipovi)
    context['preostaloOdSvakogTipa'] = json.dumps(preostaloOdSvakogTipa)
    context['cene'] = json.dumps(cene)
    context['dogadjaj_id'] = dogadjaj_id
    context['organizator_id'] = organizator_id
    context['preostaloOdSvakogTipa1'] = preostaloOdSvakogTipa
    context['prviTip'] = tipovi[0]
    return render(request, template_name='templates/dogadjaj1.html', context=context)

def pocetna(request: HttpRequest):
    '''
       @param request: HttpRequest
        @return HttpResponse
        Implementirao: Vladan Vasic, 2020/0040
        Ovo je view pocetne stranice sajta
    '''
    trenutni_datum = datetime.datetime.today()
    top_dogadjaji = Dogadjaj.objects.order_by('-organizator__prosecna_ocena').filter(
        datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc))
    if len(top_dogadjaji) <= 4:
        top_dogadjaji_prvi = top_dogadjaji
        top_dogadjaji_drugi = []
        top_dogadjaji_treci = []
    else:
        top_dogadjaji_prvi = top_dogadjaji[:4]
        if 4 < len(top_dogadjaji) <= 8:
            top_dogadjaji_drugi = top_dogadjaji[4:]
            top_dogadjaji_treci = []
        else:
            top_dogadjaji_drugi = top_dogadjaji[4:8]
            if len(top_dogadjaji) < 12:
                top_dogadjaji_treci = top_dogadjaji[8:]
            else:
                top_dogadjaji_treci = top_dogadjaji[8:12]

    pozoriste_dog = Pozoriste.objects.order_by('-organizator__prosecna_ocena').filter(
        datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).first()
    muzika_dog = Muzika.objects.order_by('-organizator__prosecna_ocena').filter(
        datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).first()
    sport_dog = Sport.objects.order_by('-organizator__prosecna_ocena').filter(
        datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).first()
    zurka_dog = Zurka.objects.order_by('-organizator__prosecna_ocena').filter(
        datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).first()
    ostalo_dog = Ostalo.objects.order_by('-organizator__prosecna_ocena').filter(
        datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).first()
    context = {
        'top_dogadjaji_prvi': top_dogadjaji_prvi,
        'top_dogadjaji_drugi': top_dogadjaji_drugi,
        'top_dogadjaji_treci': top_dogadjaji_treci,
        'pozoriste_dog': pozoriste_dog,
        'muzika_dog': muzika_dog,
        'sport_dog': sport_dog,
        'zurka_dog': zurka_dog,
        'ostalo_dog': ostalo_dog,
    }

    return render(request, template_name='templates/pocetna.html', context=context)


def sport(request: HttpRequest):
    '''
        @param request: HttpRequest
        @return HttpResponse
        Implementirao: Vladan Vasic, 2020/0040
        Ovo je view stranice sajta koja se ucitava kada korisnik klikne tab Sport u zaglavlju
    '''
    trenutni_datum = datetime.datetime.today()
    dogadjaji = Sport.objects.filter(datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).order_by(
        '-organizator__prosecna_ocena')
    context = {
        'dogadjaji': dogadjaji,
    }
    return render(request, template_name='templates/sport.html', context=context)


def sport_pretraga(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return JsonResponse
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je url koji se izvrsava kada korisnik popuni bilo koje polje za pretragu na stranici sportskih dogadajaja
    '''
    if request.method == 'POST':
        trenutni_datum = datetime.datetime.today()
        naziv = json.loads(request.body).get('naziv')
        grad = json.loads(request.body).get('grad')
        naziv_sporta = json.loads(request.body).get('naziv_sporta')
        date_range = json.loads(request.body).get('date_range')
        dogadjaji = Sport.objects.filter(
            datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).order_by(
            '-organizator__prosecna_ocena')

        pocetak, kraj = date_range.split(' - ')
        pocetak_podaci = pocetak.split('/')
        kraj_podaci = kraj.split('/')
        pocetak_datum = datetime.datetime(year=int(pocetak_podaci[2]), month=int(pocetak_podaci[0]),
                                          day=int(pocetak_podaci[1]))
        kraj_datum = datetime.datetime(year=int(kraj_podaci[2]), month=int(kraj_podaci[0]),
                                       day=int(kraj_podaci[1]))
        kraj_datum_pret = kraj_datum + datetime.timedelta(days=1)

        if pocetak_datum.date() != trenutni_datum.date() or kraj_datum.date() != trenutni_datum.date():
            dogadjaji = dogadjaji.filter(datum_vreme__gte=pocetak_datum.replace(tzinfo=datetime.timezone.utc)).filter(
                datum_vreme__lte=kraj_datum_pret.replace(tzinfo=datetime.timezone.utc))

        if naziv != '':
            dogadjaji = dogadjaji.filter(naziv__icontains=naziv)

        if naziv_sporta != '':
            dogadjaji = dogadjaji.filter(naziv_sporta__icontains=naziv_sporta)

        if grad != '':
            dogadjaji = dogadjaji.filter(grad__naziv__icontains=grad)

        data = dogadjaji.values()
        return JsonResponse(list(data), safe=False)


def muzika(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return HttpResponse
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je view stranice sajta koja se ucitava kada korisnik klikne tab Muzika u zaglavlju
    '''
    trenutni_datum = datetime.datetime.today()
    dogadjaji = Muzika.objects.filter(datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).order_by(
        '-organizator__prosecna_ocena')
    context = {
        'dogadjaji': dogadjaji,
    }
    return render(request, template_name='templates/muzika.html', context=context)


def muzika_pretraga(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return JsonResponse
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je url koji se izvrsava kada korisnik popuni bilo koje polje za pretragu na stranici muzickih dogadajaja
    '''
    if request.method == 'POST':
        trenutni_datum = datetime.datetime.today()
        naziv = json.loads(request.body).get('naziv')
        grad = json.loads(request.body).get('grad')
        izvodjac = json.loads(request.body).get('izvodjac')
        date_range = json.loads(request.body).get('date_range')
        dogadjaji = Muzika.objects.filter(
            datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).order_by(
            '-organizator__prosecna_ocena')

        pocetak, kraj = date_range.split(' - ')
        pocetak_podaci = pocetak.split('/')
        kraj_podaci = kraj.split('/')
        pocetak_datum = datetime.datetime(year=int(pocetak_podaci[2]), month=int(pocetak_podaci[0]),
                                          day=int(pocetak_podaci[1]))
        kraj_datum = datetime.datetime(year=int(kraj_podaci[2]), month=int(kraj_podaci[0]),
                                       day=int(kraj_podaci[1]))
        kraj_datum_pret = kraj_datum + datetime.timedelta(days=1)

        if pocetak_datum.date() != trenutni_datum.date() or kraj_datum.date() != trenutni_datum.date():
            dogadjaji = dogadjaji.filter(datum_vreme__gte=pocetak_datum.replace(tzinfo=datetime.timezone.utc)).filter(
                datum_vreme__lte=kraj_datum_pret.replace(tzinfo=datetime.timezone.utc))

        if naziv != '':
            dogadjaji = dogadjaji.filter(naziv__icontains=naziv)

        if izvodjac != '':
            dogadjaji = dogadjaji.filter(izvodjac__icontains=izvodjac)

        if grad != '':
            dogadjaji = dogadjaji.filter(grad__naziv__icontains=grad)
        data = dogadjaji.values()
        return JsonResponse(list(data), safe=False)


def pozoriste(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return HttpResponse
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je view stranice sajta koja se ucitava kada korisnik klikne tab Pozoriste u zaglavlju
    '''
    trenutni_datum = datetime.datetime.today()
    dogadjaji = Pozoriste.objects.filter(
        datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).order_by('-organizator__prosecna_ocena')
    context = {
        'dogadjaji': dogadjaji,
    }
    return render(request, template_name='templates/pozoriste.html', context=context)


def pozoriste_pretraga(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return JsonResponse
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je url koji se izvrsava kada korisnik popuni bilo koje polje za pretragu na stranici sa predstavama
    '''
    if request.method == 'POST':
        trenutni_datum = datetime.datetime.today()
        naziv = json.loads(request.body).get('naziv')
        zanr = json.loads(request.body).get('zanr')
        glumci = json.loads(request.body).get('glumci')
        date_range = json.loads(request.body).get('date_range')
        grad = json.loads(request.body).get('grad')
        dogadjaji = Pozoriste.objects.filter(
            datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).order_by(
            '-organizator__prosecna_ocena')

        pocetak, kraj = date_range.split(' - ')
        pocetak_podaci = pocetak.split('/')
        kraj_podaci = kraj.split('/')
        pocetak_datum = datetime.datetime(year=int(pocetak_podaci[2]), month=int(pocetak_podaci[0]),
                                          day=int(pocetak_podaci[1]))
        kraj_datum = datetime.datetime(year=int(kraj_podaci[2]), month=int(kraj_podaci[0]),
                                       day=int(kraj_podaci[1]))
        kraj_datum_pret = kraj_datum + datetime.timedelta(days=1)

        if pocetak_datum.date() != trenutni_datum.date() or kraj_datum.date() != trenutni_datum.date():
            dogadjaji = dogadjaji.filter(datum_vreme__gte=pocetak_datum.replace(tzinfo=datetime.timezone.utc)).filter(
                datum_vreme__lte=kraj_datum_pret.replace(tzinfo=datetime.timezone.utc))

        if naziv != '':
            dogadjaji = dogadjaji.filter(naziv__icontains=naziv)

        if zanr != '':
            dogadjaji = dogadjaji.filter(zanr__icontains=zanr)

        if glumci != '':
            dogadjaji = dogadjaji.filter(glumci__icontains=glumci)

        if grad != '':
            dogadjaji = dogadjaji.filter(grad__naziv__icontains=grad)

        data = dogadjaji.values()
        return JsonResponse(list(data), safe=False)


def zurka(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return HttpResponse
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je view stranice sajta koja se ucitava kada korisnik klikne tab Zurka u zaglavlju
    '''
    trenutni_datum = datetime.datetime.today()
    dogadjaji = Zurka.objects.filter(datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).order_by(
        '-organizator__prosecna_ocena')
    context = {
        'dogadjaji': dogadjaji,
    }
    return render(request, template_name='templates/zurka.html', context=context)


def zurka_pretraga(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return JsonResponse
            Implementirao: Vladan Vasic, 2020/0040
             Ovo je url koji se izvrsava kada korisnik popuni bilo koje polje za pretragu na stranici sa zurkama
    '''
    if request.method == 'POST':
        trenutni_datum = datetime.datetime.today()
        naziv = json.loads(request.body).get('naziv')
        izvodjac = json.loads(request.body).get('izvodjac')
        vrsta_muzike = json.loads(request.body).get('vrsta_muzike')
        grad = json.loads(request.body).get('grad')
        date_range = json.loads(request.body).get('date_range')
        dogadjaji = Zurka.objects.filter(
            datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).order_by(
            '-organizator__prosecna_ocena')

        pocetak, kraj = date_range.split(' - ')
        pocetak_podaci = pocetak.split('/')
        kraj_podaci = kraj.split('/')
        pocetak_datum = datetime.datetime(year=int(pocetak_podaci[2]), month=int(pocetak_podaci[0]),
                                          day=int(pocetak_podaci[1]))
        kraj_datum = datetime.datetime(year=int(kraj_podaci[2]), month=int(kraj_podaci[0]),
                                       day=int(kraj_podaci[1]))
        kraj_datum_pret = kraj_datum + datetime.timedelta(days=1)

        if pocetak_datum.date() != trenutni_datum.date() or kraj_datum.date() != trenutni_datum.date():
            dogadjaji = dogadjaji.filter(datum_vreme__gte=pocetak_datum.replace(tzinfo=datetime.timezone.utc)).filter(
                datum_vreme__lte=kraj_datum_pret.replace(tzinfo=datetime.timezone.utc))

        if naziv != '':
            dogadjaji = dogadjaji.filter(naziv__icontains=naziv)

        if izvodjac != '':
            dogadjaji = dogadjaji.filter(izvodjac__icontains=izvodjac)

        if vrsta_muzike != '':
            dogadjaji = dogadjaji.filter(vrsta_muzike__icontains=vrsta_muzike)

        if grad != '':
            dogadjaji = dogadjaji.filter(grad__naziv__icontains=grad)

        data = dogadjaji.values()
        return JsonResponse(list(data), safe=False)


def ostalo(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return HttpResponse
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je view stranice sajta koja se ucitava kada korisnik klikne tab Ostalo u zaglavlju
    '''
    trenutni_datum = datetime.datetime.today()
    dogadjaji = Ostalo.objects.filter(datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).order_by(
        '-organizator__prosecna_ocena')
    context = {
        'dogadjaji': dogadjaji,
    }
    return render(request, template_name='templates/ostalo.html', context=context)

def ostalo_pretraga(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return JsonResponse
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je url koji se izvrsava kada korisnik popuni bilo koje polje za pretragu na stranici sa ostalim dogadjajima
    '''
    if request.method == 'POST':
        trenutni_datum = datetime.datetime.today()
        naziv = json.loads(request.body).get('naziv')
        grad = json.loads(request.body).get('grad')
        date_range = json.loads(request.body).get('date_range')
        dogadjaji = Ostalo.objects.filter(
            datum_vreme__gte=trenutni_datum.replace(tzinfo=datetime.timezone.utc)).order_by(
            '-organizator__prosecna_ocena')

        pocetak, kraj = date_range.split(' - ')
        pocetak_podaci = pocetak.split('/')
        kraj_podaci = kraj.split('/')
        pocetak_datum = datetime.datetime(year=int(pocetak_podaci[2]), month=int(pocetak_podaci[0]),
                                          day=int(pocetak_podaci[1]))
        kraj_datum = datetime.datetime(year=int(kraj_podaci[2]), month=int(kraj_podaci[0]),
                                       day=int(kraj_podaci[1]))
        kraj_datum_pret = kraj_datum + datetime.timedelta(days=1)

        if pocetak_datum.date() != trenutni_datum.date() or kraj_datum.date() != trenutni_datum.date():
            dogadjaji = dogadjaji.filter(datum_vreme__gte=pocetak_datum.replace(tzinfo=datetime.timezone.utc)).filter(
                datum_vreme__lte=kraj_datum_pret.replace(tzinfo=datetime.timezone.utc))

        if naziv != '':
            dogadjaji = dogadjaji.filter(naziv__icontains=naziv)

        if grad != '':
            dogadjaji = dogadjaji.filter(grad__naziv__icontains=grad)

        data = dogadjaji.values()
        return JsonResponse(list(data), safe=False)

'''
                    @param request: HttpRequest
                    @return HttpResponse
                    Implementirao Bogdan Radosavljevic, 2020/0109
                    Narednih 4 funkcija je backend koji prikazuje komponente footer-a
'''
def oNama(request: HttpRequest):
    return render(request, template_name='templates/oNama.html')
def uslovi(request: HttpRequest):
    return render(request, template_name='templates/uslovi.html')
def privatnost(request: HttpRequest):
    return render(request, template_name='templates/privatnost.html')
def pomoc(request: HttpRequest):
    return render(request, template_name='templates/pomoc.html')

@login_required(login_url='login')
def profil(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return HttpResponse
            Implementirao: Marko Lukesevic, 2020/0246
            Ovo je view stranice sajta koja se ucitava kada korisnik klikne na svoj profil (svoju sliku)
    '''
    korisnik = request.user
    poseceni_dogadjaji = Dogadjaj.objects.filter(karta__korisnik=korisnik).distinct()
    je_organizator = korisnik.is_staff
    organizovani_dogadjaji = Dogadjaj.objects.filter(organizator=korisnik)
    recenzije = Recenzija.objects.filter(korisnik=korisnik)
    context = {
        'korisnik': korisnik,
        'poseceni_dogadjaji' : poseceni_dogadjaji,
        'je_organizator': je_organizator,
        'organizovani_dogadjaji' : organizovani_dogadjaji,
        'recenzije': recenzije
    }
    return render(request, 'templates/profil.html', context)

@login_required(login_url='login')
def recenzija(request: HttpRequest, dogadjaj_id: int):
    '''
            @param request: HttpRequest
            @param dogadjaj_id: int
            @return HttpResponse
            @throws Http404
            Implementirao: Marko Lukesevic, 2020/0246
            Ovo je view stranice sajta koja se ucitava kada korisnik klikne na dugme "ostavi recenziju" na nekom od svojih posecenih dogadjaja.
    '''
    try:
        dogadjaj = Dogadjaj.objects.get(pk=dogadjaj_id)
    except:
        raise Http404('Dogadjaj ne postoji')

    korisnik = request.user
    organizator = dogadjaj.organizator
    poseceni_dogadjaji = Dogadjaj.objects.filter(karta__korisnik=korisnik)
    if dogadjaj in poseceni_dogadjaji:
        if request.method == 'POST':
            forma = RecenzijaForm(request.POST)
            if forma.is_valid():
                komentar = forma.cleaned_data['tekst_recenzije']
                ocena = forma.cleaned_data['ocena']
                Recenzija.objects.create(
                    ocena=ocena,
                    dogadjaj=dogadjaj,
                    komentar=komentar,
                    korisnik=korisnik
                )
                trenutni_broj_recenzija = organizator.ukupno_recenzija + 1
                trenutni_zbir_ocena = organizator.zbir_ocena + int(ocena)
                prosecna_ocena = trenutni_zbir_ocena / trenutni_broj_recenzija
                organizator.zbir_ocena = trenutni_zbir_ocena
                organizator.ukupno_recenzija = trenutni_broj_recenzija
                organizator.prosecna_ocena = prosecna_ocena
                organizator.save()
            return redirect('profil')
        else:
            forma = RecenzijaForm()
            context = {
                'forma': forma,
                'dogadjaj_id': dogadjaj_id
            }
            return render(request, 'templates/ostavljanje_recenzije.html', context)
    else:
        raise Http404('Niste posetili dogadjaj i ne mozete ostaviti recenziju.')


@login_required(login_url='login')
def dogadjaj_informacije(request: HttpRequest, dogadjaj_id: int):
    '''
           @param request: HttpRequest
           @param dogadjaj_id: int
           @return HttpResponse
           @throws Http404
           Implementirao: Marko Lukesevic, 2020/0246
           Ovo je view stranice sajta koja se ucitava kada korisnik klikne na dugme "pregledaj informacije o dogadjaju" na nekom od svojih organizovanih dogadjaja.
    '''
    try:
        dogadjaj = Dogadjaj.objects.get(pk=dogadjaj_id)
    except:
        raise Http404('Dogadjaj ne postoji')

    if request.user == dogadjaj.organizator:
        recenzije = Recenzija.objects.filter(dogadjaj=dogadjaj)
        broj_prodatih_karata = Karta.objects.filter(dogadjaj=dogadjaj, status='kupljena').count()
        broj_rezervisanih_karata = Karta.objects.filter(dogadjaj=dogadjaj, status='rezervisana').count()
        broj_slobodnih_karata = Karta.objects.filter(dogadjaj=dogadjaj, status='slobodna').count()
        broj_recenzija = {
            'ukupno': Recenzija.objects.filter(dogadjaj=dogadjaj).count(),
            'ocena5': Recenzija.objects.filter(dogadjaj=dogadjaj, ocena=5).count(),
            'ocena4': Recenzija.objects.filter(dogadjaj=dogadjaj, ocena=4).count(),
            'ocena3': Recenzija.objects.filter(dogadjaj=dogadjaj, ocena=3).count(),
            'ocena2': Recenzija.objects.filter(dogadjaj=dogadjaj, ocena=2).count(),
            'ocena1': Recenzija.objects.filter(dogadjaj=dogadjaj, ocena=1).count()
        }
        context = {
            'dogadjaj': dogadjaj,
            'recenzije': recenzije,
            'broj_prodatih_karata': broj_prodatih_karata,
            'broj_rezervisanih_karata': broj_rezervisanih_karata,
            'broj_slobodnih_karata': broj_slobodnih_karata,
            'broj_recenzija' : broj_recenzija
        }
        return render(request, 'templates/dogadjaj_informacije.html', context)
    else:
        return HttpResponseForbidden("Niste autorizovani da pristupite ovim informacijama")


@login_required(login_url='login')
def azuriranje_profila(request: HttpRequest):
    '''
            @param request: HttpRequest
            @param dogadjaj_id: int
            @return HttpResponse
            Implementirao: Marko Lukesevic, 2020/0246
            Ovo je url koji se izvrsava kada korisnik pritisne dugme "azurirajte profil" na stranici svog profila
    '''
    if request.method == 'POST':
        korisnik = request.user
        ime = request.POST.get('ime')
        prezime = request.POST.get('prezime')
        email = request.POST.get('email')
        lozinka = request.POST.get('lozinka')
        try:
            if ime:
                korisnik.ime = ime
            if prezime:
                korisnik.prezime= prezime
            if email:
                korisnik.email = email
            if lozinka:
                korisnik.set_password(lozinka)
            korisnik.save()
            update_session_auth_hash(request, korisnik)
            return redirect('profil')
        except:
            return HttpResponse("Error")
    else:
        return HttpResponse("Method not allowed")

@login_required(login_url='login')
def provera_emaila(request: HttpRequest):
    '''
            @param request: HttpRequest
            @return JsonResponse
            Implementirao: Marko Lukesevic, 2020/0246
            Ovo je url koji se izvrsava prilikom azuriranja profila kada se vrsi provera da li vec postoji korisnik sa unetim e-mailom
    '''
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            Korisnik.objects.get(email=email)
            postoji_email = True
        except ObjectDoesNotExist:
            postoji_email = False

        odgovor = {
            'postoji_email': postoji_email
        }

        print(odgovor)

        return JsonResponse(odgovor)

    return JsonResponse({'error': 'Nedozvoljen metod'}, status=400)


def profil_organizatora(request: HttpRequest, organizator_id: int):
    '''
            @param request: HttpRequest
            @param organizator_id: int
            @return HttpResponse
            @throws Http404
            Implementirao: Marko Lukesevic, 2020/0246
            Ovo je view stranice sajta koja se ucitava kada korisnik poseti profil nekog od organizatora.
    '''
    try:
        organizator = Korisnik.objects.get(pk = organizator_id)
    except:
        raise Http404('Korisnik ne postoji')
    organizovani_dogadjaji = Dogadjaj.objects.filter(organizator=organizator)
    poslednje_recenzije = Recenzija.objects.filter(dogadjaj__organizator=organizator).order_by('-id')[:5]
    context = {
        'organizator' : organizator,
        'organizovani_dogadjaji':organizovani_dogadjaji,
        'poslednje_recenzije' : poslednje_recenzije
    }
    return render(request, 'templates/organizator.html', context)

