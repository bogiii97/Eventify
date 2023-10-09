import datetime

from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm



class DogadjajForm(forms.Form):
    '''
        Implementirao: Vladan Vasic, 2020/0040
        Ovo je genericka forma za kreiranje dogadjaja
    '''
    naziv = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Naziv'}))
    grad = forms.ChoiceField(choices=[(grad.id, grad.naziv) for grad in Grad.objects.all()])
    adresa = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Adresa'
    }))
    datum_vreme = forms.DateTimeField(initial=datetime.datetime.now(),widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))
    slika = forms.ImageField()
    kratak_opis = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 2,
        'cols': 50,
        'maxlength': 100,
        'placeholder': 'Kratak opis',
    }))
    opis = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5,
        'cols': 60,
        'max_length': 300,
        'placeholder': 'Opis',
    }))
    prodajno_mesto = forms.MultipleChoiceField(
        choices=[(prodajno_mesto.id, prodajno_mesto.naziv) for prodajno_mesto in ProdajnoMesto.objects.all()], required=False)

class kupacInfoForm(forms.Form):
    '''
                Implementirao: Bogdan Radosavljevic, 2020/0109
                Forma za prikupljanje informacija o kupcu
    '''
    ime = forms.CharField(max_length=30)
    prezime = forms.CharField(max_length=30)
    mejl = forms.CharField(max_length=50)
    drzava = forms.CharField(max_length=30)
    grad = forms.CharField(max_length=30)
    brojTelefona = forms.CharField(max_length=30)

class karticaInfoForm(forms.Form):
    '''
                    Implementirao: Bogdan Radosavljevic, 2020/0109
                    Forma za unos podataka sa kartice
    '''
    brojKartice = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'XXXX-XXXX-XXXX-XXXX'}))
    vaziDo = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cvc = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'xxx(x)'}))

class UpitForma(forms.ModelForm):
    class Meta:
        model = Upit
        fields = ['email', 'pitanje']



from django.utils.translation import gettext_lazy as _
from .models import Grad

from django.utils.translation import gettext_lazy as _
class KorisnikCreationForm(UserCreationForm):
    '''
        Implementirao: Mateja Milenkovic, 2020/0514
        Ovo je forma za kreiranje korisnika
    '''

    class Meta:
        model = Korisnik
        fields = ['username', 'email', 'ime', 'prezime', 'grad', 'slika', 'password1', 'password2']


    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Korisničko ime'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['ime'].widget.attrs['placeholder'] = 'Ime'
        self.fields['prezime'].widget.attrs['placeholder'] = 'Prezime'
        self.fields['password1'].widget.attrs['placeholder'] = 'Šifra'
        self.fields['password2'].widget.attrs['placeholder'] = 'Potvrda šifre'




class RecenzijaForm(forms.Form):
    '''
        Implementirao: Marko Lukesevic, 2020/0246
        Ovo je forma za ostavljanje recenzije na dogadjaj
    '''
    tekst_recenzije = forms.CharField(label='Komentar',
                                      widget=forms.Textarea(attrs={'rows': 4, 'class': 'recenzija_forma'}))
    ocena = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'recenzija_forma'})
    )





