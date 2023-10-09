'''
    Studenti koji su radili na ovom fajlu:
    Vladan Vasic, 2020/0040
'''
from django.contrib.auth.models import AbstractUser
from django.db import models

class Grad(models.Model):
    '''
            Implementirao: Vladan Vasic, 2020/0040
            Ovo ja klasa u kojoj se cuvaju svi gradovi u aplikaciji
    '''
    naziv = models.CharField(max_length=50)
    class Meta:
        db_table = 'grad'

    def __str__(self):
        return self.naziv
class Korisnik(AbstractUser):
    '''
        Implementirao: Vladan Vasic, 2020/0040
        Ovo je klasa koja ujedno predstavlja korisnika i organizatora u aplikaciji. Organizator i korisnik
        se razlikuju po tome sto pripadaju razlicitim grupama i samim tim imaju razlicite dozvole(permisije).
    '''
    first_name = None
    last_name = None
    last_login = None
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    ime = models.CharField(max_length=30)
    prezime = models.CharField(max_length=30)
    grad = models.ForeignKey(Grad, on_delete=models.RESTRICT, db_column='idGrad')
    prosecna_ocena = models.FloatField(default=0.0)
    zbir_ocena = models.IntegerField(default=0)
    ukupno_recenzija = models.IntegerField(default=0)
    slika = models.ImageField(upload_to='slike/korisnici', default='slike/korisnici/korisnikDefault.png')

    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'Korisnik'

    def __str__(self):
        return f'{self.ime} {self.prezime}'

class ProdajnoMesto(models.Model):
    '''
        Implementirao: Vladan Vasic, 2020/0040
        Ovo je tabela gde se pamte sva prodajna mesta gde mogu da se kupe karte za dogadjdje
    '''
    naziv = models.CharField(max_length=50)
    adresa = models.CharField(max_length=50)
    grad = models.ForeignKey(Grad, on_delete=models.CASCADE, db_column='idGrad')

    class Meta:
        db_table = 'prodajno_mesto'

    def __str__(self):
        return self.naziv
class Dogadjaj(models.Model):
    '''
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je generalna klasa dogadjaja koje objavljuje organizator
    '''
    naziv = models.CharField(max_length=50)
    grad = models.ForeignKey(Grad, on_delete=models.RESTRICT, db_column='idGrad')
    adresa = models.CharField(max_length=50)
    datum_vreme = models.DateTimeField()
    slika = models.ImageField(upload_to="slike/dogadjaji", default="slike/dogadjaji/dogadjajDefault.png")
    organizator = models.ForeignKey(Korisnik, on_delete=models.CASCADE, db_column='idOrg')
    status = models.CharField(max_length=50, default='planiran')
    opis = models.CharField(max_length=600)
    kratak_opis = models.CharField(max_length=100)
    prodaje_se = models.ManyToManyField(ProdajnoMesto, db_table='prodaje_se')
    class Meta:
        db_table = 'Dogadjaj'

    def __str__(self):
        return self.naziv
class Sport(Dogadjaj):
    '''
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je generalna klasa sportskih dogadjaja
    '''
    naziv_sporta = models.CharField(max_length=50)
    ucesnici = models.CharField(max_length=100)
    class Meta:
        db_table = 'sport'

class Muzika(Dogadjaj):
    '''
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je generalna klasa muzickih dogadjaja
    '''
    izvodjac = models.CharField(max_length=50)
    class Meta:
        db_table = 'muzika'

class Pozoriste(Dogadjaj):
    '''
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je generalna klasa pozorisnih dogadjaja
    '''
    zanr = models.CharField(max_length=50)
    glumci = models.CharField(max_length=100)
    trajanje = models.DurationField()
    class Meta:
        db_table = 'pozoriste'

class Zurka(Dogadjaj):
    '''
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je generalna klasa zurki
    '''
    vrsta_muzike = models.CharField(max_length=50)
    izvodjac = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'zurka'
class Ostalo(Dogadjaj):
    '''
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je generalna klasa ostalih dogadjaja
    '''
    class Meta:
        db_table = 'ostalo'

class Karta(models.Model):
    '''
        Implementirao Vladan Vasic, 2020/0040
        Ovo je klasa Karta za dogadjaj koji organizator objavljuje. Za isti dogadjaj moze postojati vise vrsta
        karata, a za svaku se pamti i korisnik koji ju je kupio(null ako jos uvek nije kupljena)
    '''
    cena = models.FloatField()
    tip = models.CharField(max_length=50)
    dogadjaj = models.ForeignKey(Dogadjaj, on_delete=models.CASCADE, db_column='idDog')
    korisnik = models.ForeignKey(Korisnik, on_delete=models.CASCADE, db_column='idKor', null=True)
    status = models.CharField(max_length=15, default='slobodna')

    class Meta:
        db_table = 'Karta'

    def __str__(self):
        return f'{self.tip} - {self.dogadjaj}'

class Recenzija(models.Model):
    '''
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je generalna klasa recenzija koju korisnici daju dogadjajima
    '''
    ocena = models.IntegerField()
    komentar = models.CharField(max_length=150)
    dogadjaj = models.ForeignKey(Dogadjaj, on_delete=models.CASCADE, db_column='idDog')
    korisnik = models.ForeignKey(Korisnik, on_delete=models.CASCADE, db_column='idKor')

    class Meta:
        db_table = 'recenzija'

    def __str__(self):
        return f'Recenzija - {self.dogadjaj}'
class Upit(models.Model):
    '''
            Implementirao: Vladan Vasic, 2020/0040
            Ovo je generalna klasa upita preko kog se postavljaju pitanja korisnickoj podrsci(adminu)
    '''
    email = models.EmailField(max_length=100)
    pitanje = models.CharField(max_length=300)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'upit'

    def __str__(self):
        return f'{self.pitanje}'