import datetime

from django.http import HttpRequest
from django.test import TestCase

from .forms import RecenzijaForm

from .forms import KorisnikCreationForm
from .models import *
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .views import logout_req
from .forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now


class KupovinaRezervacijaTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.grad1 = Grad(naziv='Beograd')
        cls.grad1.save()

        cls.korisnik1 = Korisnik(is_active=True, is_superuser=True, is_staff=False, email='vv@gmail.com',
                                 ime='Vladan', prezime='Vasic', grad=cls.grad1, username='vv')
        cls.korisnik1.set_password('123')
        cls.korisnik1.save()

        cls.dogadjaj1 = Ostalo(naziv='Dogadjaj1', grad=cls.grad1, adresa='Adresa1', datum_vreme=
        datetime.datetime.now(), organizator=cls.korisnik1, opis='Opis1', kratak_opis='KO1')
        cls.dogadjaj1.save()

        cls.dogadjaj2 = Ostalo(naziv='Dogadjaj2', grad=cls.grad1, adresa='Adresa2', datum_vreme=
        datetime.datetime.now(), organizator=cls.korisnik1, opis='Opis2', kratak_opis='KO2')
        cls.dogadjaj2.save()

        cls.karta1 = Karta(dogadjaj=cls.dogadjaj1, cena=2000.0, tip='tip1')
        cls.karta1.save()
        cls.karta2 = Karta(dogadjaj=cls.dogadjaj2, cena=1000.0, tip='tip2')
        cls.karta2.save()
        print(cls.karta2.id)

    def test_interfejs_dogadjaja(self):
        response = self.client.get('/dogadjaj/1')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Dogadjaj1")
        self.assertNotContains(response, "Dogadjaj2")
        self.assertTemplateUsed(response, 'templates/dogadjaj1.html')
        self.assertContains(response, '<button class="btn btn-light" id="kupi">Kupi kartu</button>', html=True)

    def test_kupovina_form_gost(self):
        response = self.client.get('/kupovina/1 2000 tip1 1/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Podaci o kupcu")
        self.assertContains(response, '<input type="text" name="ime" maxlength="30" required="" id="id_ime">',
                            html=True)
        self.assertContains(response, '<input type="text" name="prezime" maxlength="30" required="" id="id_prezime">',
                            html=True)
        self.assertContains(response, '<input type="text" name="mejl" maxlength="50" required="" id="id_mejl">',
                            html=True)
        self.assertTemplateUsed(response, 'templates/kupovina.html')

    def test_kupovina_form_korisnik(self):
        self.client.login(username='vv', password='123')
        response = self.client.get('/kupovina/1 2000 tip1 1/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Podaci o kupcu")
        self.assertContains(response, '<input type="text" name="ime" maxlength="30" required="" id="id_ime">', html=True)
        self.assertContains(response, '<input type="text" name="prezime" maxlength="30" required="" id="id_prezime">',
                            html=True)
        self.assertContains(response, '<input type="text" name="mejl" maxlength="50" required="" id="id_mejl">',
                            html=True)
        self.assertTemplateUsed(response, 'templates/kupovina.html')

    def test_zavrsetak_kupovina_form(self):
        self.client.login(username='vv', password='123')
        response = self.client.get('/zavrsetak/1 0 1/')
        self.assertEquals(Karta.objects.get(pk=1).korisnik_id, 1)
        self.assertEquals(Karta.objects.get(pk=1).status, 'kupljena')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Uspešno ste kupili kartu za dogadjaj!')
        self.assertTemplateUsed(response, 'templates/zavrsetakKupovine.html')

    def test_zavrsetak_rezervacija_form(self):
        response = self.client.get('/zavrsetak/2 1 2/')
        self.assertEquals(Karta.objects.get(pk=2).korisnik, None)
        self.assertEquals(Karta.objects.get(pk=2).status, 'rezervisana')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Rezervacija završena')
        self.assertTemplateUsed(response, 'templates/zavrsetakKupovine.html')

class OstavljanjeRecenzije(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.username = "test_username"
        cls.password = "test_pass123"
        cls.email = "test@gmail.com"
        cls.grad = Grad.objects.create(naziv="Beograd")

        cls.korisnik = Korisnik(is_active=True, is_superuser=True, is_staff=False, email='vv@gmail.com',
                                 ime='Vladan', prezime='Vasic', grad=cls.grad, username='vv')
        cls.korisnik.set_password('123')
        cls.korisnik.save()
        cls.dogadjaj = Ostalo(naziv='Dogadjaj', id=1, grad=cls.grad, adresa='Adresa', datum_vreme=
        datetime.datetime.now(), organizator=cls.korisnik, opis='Opis', kratak_opis='KO')

        cls.dogadjaj.save()

        cls.karta = Karta(dogadjaj=cls.dogadjaj, cena=2000.0, tip='tip1', korisnik=cls.korisnik)
        cls.karta.save()

    def test_ostavljanje_recenzije(self):

        stari_broj_recenzija = self.korisnik.ukupno_recenzija
        stari_zbir_ocena = self.korisnik.zbir_ocena

        self.client.login(username='vv', password='123')

        #self.client.post('/login/', {'username': self.username, 'password': self.password})

        form_data = {
            "tekst_recenzije" : "recenzija_test",
            "ocena" : 5
        }

        form = RecenzijaForm(data=form_data)
        self.assertTrue(form.is_valid())
        id = 1

        url = "/recenzija/" + str(id) + "/"

        response = self.client.post(url, form_data)
        self.assertTrue(Recenzija.objects.filter(komentar="recenzija_test").count(), 1)

        self.assertFalse(self.korisnik.ukupno_recenzija, stari_broj_recenzija)
        self.assertFalse(self.korisnik.zbir_ocena, stari_zbir_ocena)




class AzuriranjeProfila(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.grad = Grad.objects.create(naziv="Beograd")
        cls.user = Korisnik(is_active=True, is_superuser=True, is_staff=False, email='test@gmail.com',
                             ime='TestIme', prezime='TestPrezime', grad=cls.grad, username='testuser')

        cls.user.set_password('testpassword')
        cls.user.save()

    def test_azuriranje_profila(self):


        self.client.login(username='testuser', password='testpassword')

        response = self.client.post('/profil/azuriranje_profila',
                {'ime': 'Novo ime', 'prezime': 'Novo prezime', 'email': 'noviemail@example.com','lozinka': 'novasifra123'}
        )


        self.assertEqual(response.status_code, 302)  # Provera preusmeravanja na 'profil'
        self.user.refresh_from_db()
        self.assertEqual(self.user.ime, 'Novo ime')
        self.assertEqual(self.user.prezime, 'Novo prezime')
        self.assertEqual(self.user.email, 'noviemail@example.com')
        self.assertTrue(self.user.check_password('novasifra123'))




class RegistracijaLoginTest(TestCase):
    '''
               Implementirao: Marko Lukesevic, 2020/0246
               Ovo je klasa koja predstavlja testove za Registraciju, Login i Logout
    '''
    @classmethod
    def setUpTestData(cls):
        cls.grad1 = Grad.objects.create(naziv='Beograd')

        cls.korisnik_group = Group.objects.create(name='korisnik')

        cls.username = 'testuser'
        cls.password = 'testpass123'
        cls.korisnik = Korisnik.objects.create_user(
            username=cls.username,
            password=cls.password,
            grad=cls.grad1,
            email='testuser@mail.com',
            ime='Test',
            prezime='User'
        )

    def test_registracija(self):
        form_data = {
            'username': 'testuser2',
            'email': 'testuser2@mail.com',
            'ime': 'Test',
            'prezime': 'User',
            'grad': self.grad1.id,
            'slika': '',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = KorisnikCreationForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

        response = self.client.post('/register/', form_data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Korisnik.objects.filter(username='testuser').count(), 1)

    def test_login(self):
        response = self.client.post('/login/', {'username': self.username, 'password': self.password})
        self.assertEquals(response.status_code, 302)
        self.assertTrue(response.url.endswith('/'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)

        self.assertTrue('_auth_user_id' in self.client.session)

        request = self.client.post('/logout/')

        self.assertFalse('_auth_user_id' in self.client.session)

class objavaDogadjajaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.grad = Grad(naziv='Beograd')
        cls.grad.save()

        cls.korisnik = Korisnik(is_active=True, is_superuser=True, is_staff=False, email='bogi@gmail.com',
                                 ime='Bogdan', prezime='Radosavljevic', grad=cls.grad, username='bogi')
        cls.korisnik.set_password('123')
        cls.korisnik.save()

        cls.prodajno_mesto = ProdajnoMesto.objects.create(naziv='Mesto 1', adresa="Adresa1", grad=cls.grad)
        cls.prodajno_mesto.save()

    def test_form_create_and_validity(self):
        with open('Aplikacija/static/admin.png', 'rb') as file:
            image = SimpleUploadedFile(name='admin.png', content=file.read(), content_type='image/png')

        data = {
            'naziv': 'Test Dogadjaj',
            'grad': self.grad.id,
            'adresa': 'Test Adresa',
            'datum_vreme': now(),
            'kratak_opis': 'Test Kratak Opis',
            'opis': 'Test Opis',
            'prodajno_mesto': [self.prodajno_mesto.id]
        }
        files = {
            'slika': image
        }

        form = DogadjajForm(data=data, files=files)

        if not form.is_valid():
            print(form.errors)

        self.assertTrue(form.is_valid())

    def test_create_karta_and_dogadjaj(self):
        with open('Aplikacija/static/admin.png', 'rb') as file:
            image = SimpleUploadedFile(name='admin.png', content=file.read(), content_type='image/png')

        self.dogadjaj = Dogadjaj.objects.create(
            naziv='Test Dogadjaj',
            grad=self.grad,
            adresa='Test Adresa',
            datum_vreme=now(),
            slika=image,
            organizator=self.korisnik,
            status='planiran',
            opis='Test Opis',
            kratak_opis='Test Kratak Opis',
        )
        self.dogadjaj.prodaje_se.add(self.prodajno_mesto)

        self.assertEqual(Dogadjaj.objects.count(), 1)

        #-------------------------------------------------

        self.karta = Karta.objects.create(
            dogadjaj= self.dogadjaj,
            status='slobodna',
            cena=2000.0,
            tip='tip1'
        )
        self.assertEqual(Karta.objects.count(), 1)


    def test_objavi_dogadjaj_form(self):
        self.client.login(username='bogi', password='123')
        response = self.client.post('/objava_dogadjaja/')
        self.assertEquals(response.status_code, 200)

        self.assertContains(response, '<button type="submit" class="btn btn-success">Objavi događaj</button>', html=True)
        self.assertContains(response, '<button type="submit" class="btn btn-light" id="novaKartaDugme">Novi tip karte</button>',
                            html=True)
        self.assertContains(response, 'id="id_naziv"')
        self.assertContains(response, 'id="id_grad"')
        self.assertContains(response, 'id="id_adresa"')
        self.assertContains(response, 'id="id_datum_vreme"')
        self.assertContains(response, 'id="id_slika"')
        self.assertContains(response, 'id="id_kratak_opis"')
        self.assertContains(response, 'id="id_opis"')

        self.assertTemplateUsed(response, 'templates/objava_dogadjaja.html')


    def test_form_fields_required(self):
        form = DogadjajForm()

        self.assertEqual(form.fields['naziv'].required, True)
        self.assertEqual(form.fields['grad'].required, True)
        self.assertEqual(form.fields['adresa'].required, True)
        self.assertEqual(form.fields['datum_vreme'].required, True)
        self.assertEqual(form.fields['slika'].required, True)
        self.assertEqual(form.fields['kratak_opis'].required, True)
        self.assertEqual(form.fields['opis'].required, True)

    def test_kreiraj_dogadjaj_form(self):
        self.client.login(username='bogi', password='123')

        with open('Aplikacija/static/admin.png', 'rb') as file:
            image = SimpleUploadedFile(name='admin.png', content=file.read(), content_type='image/png')

        response = self.client.post('/kreiranje_dogadjaja/', {
            'naziv': 'Test Dogadjaj',
            'grad': self.grad.id,
            'adresa': 'Test Adresa',
            'datum_vreme': now(),
            'kratak_opis': 'Test Kratak Opis',
            'opis': 'Test Opis',
            'prodajno_mesto': [self.prodajno_mesto.id],
            'slika': image,
            'cena': ['100', '200'],
            'tip': ['Tip1', 'Tip2'],
            'broj': ['1', '2']
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Dogadjaj.objects.count(), 1)
        self.assertEqual(Dogadjaj.objects.first().naziv, 'Test Dogadjaj')
        self.assertEqual(Dogadjaj.objects.first().grad, self.grad)
        self.assertEqual(Dogadjaj.objects.first().adresa, 'Test Adresa')
        self.assertEqual(Dogadjaj.objects.first().kratak_opis, 'Test Kratak Opis')
        self.assertEqual(Dogadjaj.objects.first().prodaje_se.first().id, self.prodajno_mesto.id)

        #------------------------------------------------------

        self.assertEqual(Karta.objects.count(), 3)
        dogadjaj = Dogadjaj.objects.first()
        for karta in Karta.objects.all():
            self.assertEqual(karta.dogadjaj, dogadjaj)
            self.assertEqual(karta.status, "slobodna")

        karte = list(Karta.objects.order_by('tip'))
        self.assertEqual(karte[0].cena, 100)
        self.assertEqual(karte[0].tip, 'Tip1')
        self.assertEqual(karte[1].cena, 200)
        self.assertEqual(karte[1].tip, 'Tip2')
        self.assertEqual(karte[2].cena, 200)
        self.assertEqual(karte[2].tip, 'Tip2')