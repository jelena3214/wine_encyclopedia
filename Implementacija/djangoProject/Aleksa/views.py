import datetime
from xmlrpc.client import DateTime

from django.contrib.auth.decorators import *
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userApp.decorators import group_required
from baza.models import *

# from project_FourDesperados.Implementacija.djangoProject.baza.models import *
#
@login_required(login_url='/user')
@group_required("Proizvodjaci")
def viewWine(request : HttpRequest):

    if request.method == "POST":
        print(request.POST)

        # kreiranje ponude
        new_offer = Ponuda()
        new_offer.idkorisnik = request.user
        new_offer.save()

        # unos vina
        new_wine = Vino()
        new_wine.naziv = request.POST['wineName']
        new_wine.cena = request.POST['price']
        new_wine.brojprodatih = 0
        new_wine.opisvina = request.POST['description']
        new_wine.idponuda = new_offer
        new_wine.save()

        #kreiranje slika
        new_picture = Slika()
        new_picture.slika = request.FILES["winePicture"]
        new_picture.idponuda = new_offer
        new_picture.save()


        tags = request.POST['taginputs']
        taglist = tags.split(',')
        for tag in taglist:
            if tag == "":
                continue
            new_tag = Tag()
            new_tag.idponuda = new_wine
            new_tag.tag = tag
            new_tag.save()

        context = {
            "message_body": "Vino je uspesno uneto."
        }
        return render(request, "modalMesesage.html", context)
    return render(request,"unosVina.html")


@login_required(login_url='/user')
@group_required("Proizvodjaci")
def inputTour(request : HttpRequest):
    return unosObilaskaExit(request)


@login_required(login_url='/user')
@group_required("Proizvodjaci")
def addTourType(request):


    if request.method == "POST":
        tour = checkIfTourExists(request)

        new_tour_type = Vrstaobilaska()
        new_tour_type.idponuda = tour
        new_tour_type.opis = request.POST['tourDescription']
        new_tour_type.naziv = request.POST['tourName']
        new_tour_type.cena = request.POST['tourPrice']
        new_tour_type.save()
        context = {
            "message_body": "Vrsta obilaska je uspesno dodata! Klikom na dugme vraticete se na vašu prodavnicu."
        }
        return render(request,"modalMesesage.html",context)

    return unosObilaskaExit(request)

@login_required(login_url='/user')
@group_required("Proizvodjaci")
def inputTourPicture(request):
    tour = checkIfTourExists(request)

    if request.method == "POST":
        print(request.POST)
        new_picture = Slika()
        new_picture.idponuda = tour.idponuda.idponuda
        new_picture.slika = request.FILES['inputTourPicture']
        new_picture.save()


    tour_types = Vrstaobilaska.objects.filter(idponuda=tour)
    context = {
        'obilasci': tour_types
    }
    return render(request, "unosObilaska.html", context)


@login_required(login_url='/user')
@group_required("Proizvodjaci")
def removeTourPicture(request, picture_id):

    picture_to_remove = Slika.objects.filter(idslika=picture_id)
    picture_to_remove.delete()


    return redirect('myStore')



@login_required(login_url='/user')
@group_required("Proizvodjaci")
def inputCelebration(request):

    if request.method == "POST":
        print(request.POST)
        context = {
            "message_body" : "Proslava je uspesno dodata! Klikom na dugme vraticete se na vašu prodavnicu."
        }
        new_celebration = checkIfCelebrationExists(request)

        new_celebration.cenapoosobi = request.POST['price']
        new_celebration.kapacitet = request.POST['capacity']
        new_celebration.opisproslave = request.POST['description']
        picture = Slika.objects.get(idponuda=new_celebration.idponuda.idponuda)
        picture.slika = request.FILES['inputTourPicture']
        new_celebration.save()
        picture.save()

        return render(request,"modalMesesage.html",context)


    return render(request,"unosProslave.html")


def checkIfCelebrationExists(request: HttpRequest):


    celebrations = Proslava.objects.filter(idponuda__idponuda__idkorisnik=request.user)

    if celebrations.exists():
        return Proslava.objects.get(idponuda__idponuda__idkorisnik=request.user)
    else:

        new_offer = Ponuda()
        new_offer.idkorisnik = request.user
        new_offer.save()

        new_space_offer = Ponudaprostor()
        new_space_offer.idponuda = new_offer
        new_space_offer.save()

        new_celebration = Proslava()
        if request.method == "POST":
            new_celebration.cenapoosobi = request.POST['price']
            new_celebration.kapacitet = request.POST['capacity']
            new_celebration.opisproslave = request.POST['description']

        new_celebration.idponuda = new_space_offer
        new_picture = Slika()
        if request.method == "POST":
            new_picture.slika = request.FILES['inputTourPicture']
        new_picture.idponuda = new_offer
        new_picture.save()
        new_celebration.save()


@login_required(login_url='/user')
@group_required("Proizvodjaci")
def setTourDetails(request: HttpRequest):

    tour = checkIfTourExists(request)
    tour_types = Vrstaobilaska.objects.filter(idponuda=tour)
    print(tour_types)
    if tour_types.exists():
        context = {
            "message_body": "Morate imati barem jednu vrstu obilaska unetu! Klikom na dugme vraticete se na vašu prodavnicu."
        }

    if request.method == "POST":

        tour = checkIfTourExists(request)
        tour.cenasomelijera = request.POST['sommelierPrice']
        tour.save()

        context = {
            "message_body": "Informacije o obilasku su uspesno sacuvane! Klikom na dugme vraticete se na vašu prodavnicu."
        }
        return render(request, "modalMesesage.html", context)


        print(request.POST)
    return unosObilaskaExit(request)

@login_required(login_url='/user')
@group_required("Proizvodjaci")
def addSommelier(request : HttpRequest):
    if request.method == "POST":

        tour = checkIfTourExists(request)
        new_sommelier = Somelijer()
        new_sommelier.ime = request.POST['sommelierName']
        new_sommelier.biografija = request.POST['sommelierDescription']
        new_sommelier.idponuda = tour
        new_sommelier.slika = request.FILES['sommelierPicture']
        new_sommelier.save()

    return redirect('inputTour')

def checkIfTourExists(request : HttpRequest):

    tours = Obilazak.objects.filter(idponuda__idponuda__idkorisnik=request.user)

    if tours.exists():
        return tours.get(idponuda__idponuda__idkorisnik=request.user)
    else:
        new_offer = Ponuda()
        new_offer.idkorisnik = request.user
        new_offer.save()
        new_space_offer = Ponudaprostor()
        new_space_offer.idponuda = new_offer
        new_space_offer.save()
        new_tour = Obilazak()
        new_tour.idponuda = new_space_offer
        new_tour.save()
        return new_tour

def unosObilaskaExit(request : HttpRequest):
    tour = checkIfTourExists(request)
    tour_types = Vrstaobilaska.objects.filter(idponuda=tour)
    sommeliers = Somelijer.objects.filter(idponuda=tour)

    context = {
        'obilasci': tour_types,
        'somelijeri' : sommeliers
    }
    return render(request, "unosObilaska.html", context)

@login_required(login_url='/user')
@group_required("Proizvodjaci")
def removeTourType(request : HttpRequest, value):

    tour_type_to_remove = Vrstaobilaska.objects.get(idobilazak=int(value))
    tour_type_to_remove.delete()

    return redirect("inputTour")

@login_required(login_url='/user')
@group_required("Proizvodjaci")
def removeSommelier(request: HttpRequest,value):

    sommelier_to_remove = Somelijer.objects.get(idsomelijer=int(value))
    sommelier_to_remove.delete()

    return redirect('inputTour')

@login_required(login_url='/user')
@group_required("Proizvodjaci")
def myStore(request):
    tour = checkIfTourExists(request)
    celebrations = []
    pictures = []
    reserved_tours = []
    reserved_tours_tuple = []
    reserved_celebrations_tuple = []
    if tour:
        pictures = Slika.objects.filter(idponuda=tour.idponuda.idponuda)
        reserved_tours = Termin.objects.filter(idponuda=tour.idponuda)
        for reservation in reserved_tours:
            tour_user = Rezervacija.objects.get(idtermin=reservation.idtermin)
            reserved_tours_tuple.append([reservation,tour_user])



    celebration = checkIfCelebrationExists(request)
    if celebration:
        celebrations = Termin.objects.filter(idponuda=celebration.idponuda)
        for reservation in celebrations:
            celebration_user = Rezervacija.objects.get(idtermin=reservation.idtermin)
            reserved_celebrations_tuple.append([reservation, celebration_user])





    wines = Vino.objects.filter(idponuda__idkorisnik=request.user)

    wine_tuple = []
    for wine in wines:
        picture = Slika.objects.get(idponuda=wine.idponuda)
        wine_tuple.append([wine,picture])


    context = {
        'pictures' : pictures,
        'celebrations' : reserved_celebrations_tuple,
        'resrved_tours' : reserved_tours_tuple,
        'wines' : wine_tuple
    }
    return render(request, "mojaProdavnica.html", context)

@login_required(login_url='/user')
@group_required("Proizvodjaci")
def removeReservation(request, reservation_id):

    reservation_to_delete = Termin.objects.get(idtermin=reservation_id)
    reservation_to_delete.delete()

    return redirect("myStore")

@login_required(login_url='/user')
@group_required("Proizvodjaci")
def removeWine(request,wine_id):

    wine_to_remove = Vino.objects.get(idponuda=wine_id)
    wine_to_remove.delete()

    return redirect("myStore")



@login_required(login_url='/user')
@group_required("Proizvodjaci")
def viewAds(request : HttpRequest):

    return adsExit(request)

@login_required(login_url='/user')
@group_required("Proizvodjaci")
def unsubscribeAd(request: HttpRequest, ad_id):

    ad_to_remove = Pretplacen.objects.get(idpretplata=ad_id,idkorisnik=request.user)
    ad_to_remove.trenutnistatus = 'Istekla'
    ad_to_remove.save()
    # ad_to_remove.delete()


    return redirect('viewAds')

@login_required(login_url='/user')
@group_required("Proizvodjaci")
def subscribeAd(request: HttpRequest, ad_id):

    active_ads = Pretplacen.objects.filter(idkorisnik=request.user,trenutnistatus='Aktivna')

    if active_ads.exists():
        context = {
            "message_body": "Ne mozete imati vise od jedne pretplate."
        }
        return render(request, "modalMesesage.html", context)

    new_subscription = Pretplacen()
    new_subscription.idkorisnik = request.user
    new_subscription.datumpocetak = datetime.date.today()
    new_subscription.datumkraj = datetime.date.today()
    new_subscription.datumkraj.replace(year=new_subscription.datumkraj.year + 1)
    new_subscription.idpretplata = Pretplata.objects.get(idpretplata=ad_id)
    new_subscription.trenutnistatus = 'Aktivna'
    new_subscription.save()

    return redirect('viewAds')



def adsExit(request):
    ads_not_subscribed_to = Pretplata.objects.exclude(pretplacen__idkorisnik=request.user)
    ads_subscribed_to = Pretplata.objects.filter(pretplacen__idkorisnik=request.user,pretplacen__trenutnistatus='Aktivna')
    old_ads = Pretplata.objects.filter(pretplacen__idkorisnik=request.user,pretplacen__trenutnistatus='Istekla')


    context = {'ads_not_subscribed_to': ads_not_subscribed_to,
               'ads_subscribed_to' : ads_subscribed_to,
               'old_ads' : old_ads
               }
    return render(request, "unosReklame.html", context)