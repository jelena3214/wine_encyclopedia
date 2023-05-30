from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from baza.models import *
from random import choice, choices
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import Client

from shopping.views import findImagePath


class TempVino:
    def __init__(self, naziv, opis, cena, slika, id):
        self.naziv = naziv
        self.cena = cena
        self.slika = slika
        self.opis = opis
        self.id = id


class TempRecenzija:
    def __init__(self, tekst, ocena, ime):
        self.tekst = tekst
        self.ocena = ocena
        self.ime = ime


class TempProstor:
    def __init__(self, ime, slika):
        self.ime = ime
        self.slika = slika


class TempProslava:
    def __init__(self, ime, slika, id):
        self.ime = ime
        self.slika = slika  # niz slika
        self.id = id


def viewWines(request):
    wines = Vino.objects.all()
    tags = list(Tag.objects.all().values('tag').distinct())
    listOfTags = []
    for tag in tags:
        listOfTags.append(tag["tag"])
    rowsOfWines = []
    row = []

    if request.method == 'POST' and request.POST.get('filter') != None:
        filter = request.POST.get('filter')
        tags = Tag.objects.filter(tag=filter)
        offers = []
        for tag in tags:
            offer = Vino.objects.filter(idponuda=tag.idponuda_id).first()
            offers.append(offer)

        forCnt = 0
        for wine in offers:
            pictures = Slika.objects.filter(idponuda=wine.idponuda_id)
            tmp = TempVino(wine.naziv, wine.opisvina, wine.cena, pictures[0].slika, wine.idponuda_id)
            row.append(tmp)
            if (forCnt % 3 == 0 and forCnt != 0) or (len(offers) <= 3 and forCnt == len(offers) - 1):
                rowsOfWines.append(row)
                row = []
            forCnt += 1
    else:
        forCnt = 0
        for wine in wines:
            pictures = Slika.objects.filter(idponuda=wine.idponuda_id)
            tmp = TempVino(wine.naziv, wine.opisvina, wine.cena, pictures[0].slika, wine.idponuda_id)
            row.append(tmp)
            if forCnt % 3 == 0 and forCnt != 0 or (len(wines) <= 3 and forCnt == len(wines) - 1):
                rowsOfWines.append(row)
                row = []
            forCnt += 1

    context = {
        'vina': rowsOfWines,
        'tagovi': listOfTags
    }

    return render(request, "pregledVina.html", context)


def wine(request, value):
    id = int(value[1:])
    if request.method == 'POST' and request.user.is_authenticated:
        mark = request.POST.get('rate')
        user = request.user
        text = request.POST.get('recenzija')
        newReview = Recenzija(idponuda=Ponuda(idponuda=id, idkorisnik_id=user), idkorisnik_id=user.id,
                              opisrec=text, ocena=mark)
        newReview.save()
        return redirect("/views/wine/" + value)

    wine = Vino.objects.filter(idponuda=id)
    tmp = None
    tags = []
    reviews = []
    if wine:
        wine = wine[0]
        pictures = Slika.objects.filter(idponuda=id)
        tag = Tag.objects.filter(idponuda=id)
        review = Recenzija.objects.filter(idponuda=id)
        if review:
            for r in review:
                ocena = []
                user = Korisnik.objects.filter(id=r.idkorisnik_id)
                if user != None:
                    for i in range(r.ocena):
                        ocena.append("+")
                    reviews.append(TempRecenzija(r.opisrec, ocena, user[0].javnoime))
        if tag:
            for t in tag:
                tags.append(t.tag)
        if len(pictures) != 0:
            tmp = TempVino(wine.naziv.capitalize(), wine.opisvina, wine.cena, pictures[0].slika, wine.idponuda_id)

    context = {
        'vino': tmp,
        'tag': tags,
        'recenzije': reviews,
    }
    return render(request, "vinoPojedinacanPrikaz.html", context)


def detour(request):
    offer = Ponuda.objects.all()
    tours = Obilazak.objects.all()
    rowsOfTours = []
    row = []
    forCnt = 0

    for tour in tours:
        o = offer.filter(idponuda=tour.idponuda_id)
        winery = Korisnik.objects.filter(email=o[0].idkorisnik)[0].javnoime
        picture = Slika.objects.filter(idponuda=tour.idponuda_id)[0].slika
        tmp = TempProstor(winery, picture)
        row.append(tmp)
        if (forCnt % 3 == 0 and forCnt != 0) or (len(tours) <= 3 and forCnt == len(tours) - 1):
            rowsOfTours.append(row)
            row = []
        forCnt += 1

    context = {
        'obilasci': rowsOfTours
    }

    return render(request, "pregledObilazaka.html", context)


def oneDetour(request, value):
    name = value[1:]
    users = Korisnik.objects.filter(javnoime=name)
    winery = None
    for user in users:
        pr = Proizvodjac.objects.filter(email=user.email)
        if pr is not None:
            winery = pr[0]
            break
    offers = Ponuda.objects.filter(idkorisnik_id=winery.id)
    offer = None
    tours = Obilazak.objects.all()
    for o in offers:
        pr = tours.filter(idponuda=o.idponuda)
        if len(pr):
            offer = pr[0]
    if offer is None:
        return celebration(request)

    typesOfTour = Vrstaobilaska.objects.filter(idponuda=offer.idponuda.idponuda_id)
    pictures = Slika.objects.filter(idponuda=offer.idponuda.idponuda_id)
    slika = findImagePath(pictures[0].slika)
    sommeliers = Somelijer.objects.filter(idponuda=offer.idponuda.idponuda_id)
    context = {
        'vinarija': winery,
        'obilasci': typesOfTour,
        'slika': slika,
        'somelijeri': sommeliers
    }
    return render(request, "obilazakPojedinacanPrikaz.html", context)


def celebration(request):
    offer = Ponuda.objects.all()
    celebrations = Proslava.objects.all()
    rowsOfCelebrations = []
    row = []
    forCnt = 0

    for celebration in celebrations:
        c = offer.filter(idponuda=celebration.idponuda_id)
        winery = Korisnik.objects.filter(email=c[0].idkorisnik)[0].javnoime
        pictures = Slika.objects.filter(idponuda=celebration.idponuda_id)
        tmp = TempProstor(winery, pictures[0].slika)
        row.append(tmp)
        if (forCnt % 3 == 0 and forCnt != 0) or (len(celebrations) <= 3 and forCnt == len(celebrations) - 1):
            rowsOfCelebrations.append(row)
            row = []
        forCnt += 1

    context = {
        'proslave': rowsOfCelebrations
    }

    return render(request, "pregledProslava.html", context)


def oneCelebration(request, value):
    name = value[1:]
    users = Korisnik.objects.filter(javnoime=name)
    winery = None
    for user in users:
        producer = Proizvodjac.objects.filter(email=user.email)
        if producer is not None:
            winery = producer[0]
            break
    offers = Ponuda.objects.filter(idkorisnik_id=winery.id)
    offer = None
    celebrations = Proslava.objects.all()
    for off in offers:
        pr = celebrations.filter(idponuda=off.idponuda)
        if len(pr):
            offer = pr[0]
    if offer is None:
        return celebration(request)

    pics = Slika.objects.filter(idponuda=offer.idponuda.idponuda_id)
    pictures = []
    for pic in pics:
        pictures.append(pic.slika)

    context = {
        'vinarija': winery,
        'slike': pictures,
        'ponuda': offer
    }

    print(pictures)
    return render(request, "proslavaPojedinacanPrikaz.html", context)


def home(request):
    subscribedBasicYearly = Pretplacen.objects.filter(idpretplata=1)
    subscribedBasicMonthly = Pretplacen.objects.filter(idpretplata=3)
    subscribedBasic = []
    for sub in subscribedBasicYearly:
        subscribedBasic.append(Korisnik.objects.get(id=sub.idkorisnik_id))
    for sub in subscribedBasicMonthly:
        subscribedBasic.append(Korisnik.objects.get(id=sub.idkorisnik_id))

    subscribedPremiumYearly = Pretplacen.objects.filter(idpretplata=2)
    subscribedPremiumMonthly = Pretplacen.objects.filter(idpretplata=4)
    subscribedPremium = []
    for sub in subscribedPremiumYearly:
        subscribedPremium.append(Korisnik.objects.get(id=sub.idkorisnik_id))
    for sub in subscribedPremiumMonthly:
        subscribedPremium.append(Korisnik.objects.get(id=sub.idkorisnik_id))

    premiumSubscriber = choice(list(subscribedPremium))
    basicSubscribers = []
    if len(list(subscribedBasic)) > 6:
        basicSubscribers = choices(list(subscribedBasic), k=6)
    else:
        basicSubscribers = list(subscribedBasic)

    if premiumSubscriber is None:
        allProducers = Proizvodjac.objects.all()
        premiumSubscriber = choice(list(allProducers))
    else:
        premiumSubscriber = Proizvodjac.objects.get(korisnik_ptr_id=premiumSubscriber.id)

    one = False
    two = False
    if len(basicSubscribers) == 1:
        one = True
    elif len(basicSubscribers) == 2:
        two = True

    winesToShow = []  # from basic subscribers choose one wine to show

    for subscriber in basicSubscribers:
        offers = Ponuda.objects.filter(idkorisnik=subscriber.id)
        wines = []

        for offer in offers:  # all offers from one subscriber
            w = Vino.objects.filter(idponuda=offer.idponuda)  # check if this offer is also a wine
            if len(list(w)) != 0:
                wines.append(w[0])  # if it is wine add to wines
        wine = choice(wines)  # choose only one wine to show
        winesToShow.append(wine)

    rowsOfWine = []
    row = []
    forCnt = 0
    for wine in winesToShow:
        picture = Slika.objects.get(idponuda=wine.idponuda).slika
        tmp = TempVino(wine.naziv, wine.opisvina, wine.cena, picture, wine.idponuda_id)
        row.append(tmp)
        if (forCnt % 3 == 0 and forCnt != 0) or (len(winesToShow) <= 3 and forCnt == len(winesToShow) - 1):
            rowsOfWine.append(row)
            row = []
        forCnt += 1

    context = {
        "premium": premiumSubscriber,
        'one': one,
        'two': two,
        "wines": rowsOfWine
    }
    return render(request, "pocetna.html", context)
