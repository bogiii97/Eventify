from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', pocetna, name='pocetna'),
    path('objava_dogadjaja/', objava_dogadjaja, name='objava_dogadjaja'),
    path('kreiranje_dogadjaja/', kreiranje_dogadjaja, name='kreiranje_dogadjaja'),
    path('login/', login_req, name='login'),
    path('dogadjaj/<int:dogadjaj_id>', dogadjaj, name='dogadjaj'),
    path('kupovina/<str:tekst>/', kupovina, name='kupovina'),
    path('zavrsetak/<str:tekst>/', zavrsetak, name='zavrsetak'),
    path('register/', registration, name='register'),
    path('logout/', logout_req, name='logout'),
    path('postavi_upit/', postavi_upit, name='postavi_upit'),

    path('profil/', profil, name='profil'),
    path('recenzija/<int:dogadjaj_id>/', recenzija, name='recenzija'),
    path('profil/<int:organizator_id>/', profil_organizatora, name='profil_organizatora'),
    path('profil/dogadjaj_informacije/<int:dogadjaj_id>', dogadjaj_informacije, name='dogadjaj_informacije'),
    path('sport/', sport, name='sport'),
    path('sport_pretraga/', csrf_exempt(sport_pretraga), name='sport_pretraga'),
    path('muzika/', muzika, name='muzika'),
    path('muzika_pretraga/', csrf_exempt(muzika_pretraga), name='muzika_pretraga'),
    path('pozoriste/', pozoriste, name='pozoriste'),
    path('pozoriste_pretraga/', csrf_exempt(pozoriste_pretraga), name='pozoriste_pretraga'),
    path('zurka/', zurka, name='zurka'),
    path('zurka_pretraga/', csrf_exempt(zurka_pretraga), name='zurka_pretraga'),
    path('ostalo/', ostalo, name='ostalo'),
    path('ostalo_pretraga/', csrf_exempt(ostalo_pretraga), name='ostalo_pretraga'),
    path('oNama/', oNama, name='oNama'),
    path('uslovi/', uslovi, name='uslovi'),
    path('privatnost/', privatnost, name='privatnost'),
    path('pomoc/', pomoc, name='pomoc'),
    path('profil/azuriranje_profila', azuriranje_profila, name='azuriranje_profila'),
    path('profil/azuriranje_profila/provera_emaila', provera_emaila, name='provera_emaila')

]