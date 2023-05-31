from django.shortcuts import render, redirect
from baza.models import *
from random import choice, choices
from shopping.views import findImagePath
from .forms import *


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


filtered = None
sorted = None


def viewWines(request):
    global sorted, filtered
    sortToDisplay = None
    wines = Vino.objects.all()
    tags = list(Tag.objects.all().values('tag').distinct())
    listOfTags = []
    for tag in tags:
        listOfTags.append(tag["tag"])

    rowsOfWines = []
    row = []
    filter = request.POST.get('filter')
    sort = request.POST.get('sort')
    ids = []

    if filter == '':
        filtered = None

    if sort == '':
        sorted = None

    if request.method == 'POST':
        offers = []
        if filter:
            filtered = filter
            winesTags = Tag.objects.filter(tag=filter)
            for tag in winesTags:
                offer = Vino.objects.filter(idponuda=tag.idponuda_id).first()
                ids.append(offer.idponuda_id)
                offers.append(offer)

            if sorted == 'Po ceni rastuce':
                queryset = Vino.objects.filter(idponuda__in=ids).order_by('cena')
                offers = list(queryset)
            elif sorted == 'Po ceni opadajuce':
                queryset = Vino.objects.filter(idponuda__in=ids).order_by('-cena')
                offers = list(queryset)
        if filtered is None:
            queryset = Vino.objects.all()
            if sorted == 'Po ceni rastuce':
                queryset = queryset.order_by('cena')
                offers = list(queryset)
            elif sorted == 'Po ceni opadajuce':
                queryset = queryset.order_by('-cena')
                offers = list(queryset)
        if sort:
            sorted = sort
            if sort == 'Po ceni rastuce':
                sortToDisplay = "Po ceni opadajuce"
                if filtered:
                    offers = list(Vino.objects.filter(idponuda__in=ids).order_by('cena'))
                else:
                    offers = list(Vino.objects.all().order_by('cena'))
            else:
                sortToDisplay = "Po ceni rastuce"
                if filtered:
                    offers = list(Vino.objects.filter(idponuda__in=ids).order_by('-cena'))
                else:
                    offers = list(Vino.objects.all().order_by('-cena'))
        else:
            print(offers)
        forCnt = 0
        for wine in offers:
            pictures = Slika.objects.filter(idponuda=wine.idponuda_id)
            picture = pictures[0].slika
            tmp = TempVino(wine.naziv, wine.opisvina, wine.cena, picture, wine.idponuda_id)
            row.append(tmp)
            if (forCnt % 3 == 0 and forCnt != 0) or (len(offers) <= 3 and forCnt == len(offers) - 1):
                rowsOfWines.append(row)
                row = []
            forCnt += 1

    else:
        filtered = None
        sorted = None
        forCnt = 0
        for wine in wines:
            pictures = Slika.objects.filter(idponuda=wine.idponuda_id)
            tmp = TempVino(wine.naziv, wine.opisvina, wine.cena, pictures[0].slika, wine.idponuda_id)
            row.append(tmp)
            if forCnt % 3 == 0 and forCnt != 0 or (len(wines) <= 3 and forCnt == len(wines) - 1):
                rowsOfWines.append(row)
                row = []
            forCnt += 1

    if filter:
        listOfTags.remove(filter)

    print(sorted)
    context = {
        'vina': rowsOfWines,
        'tagovi': listOfTags,
        'filter': filtered,
        'sort1': sortToDisplay,
        'sort': sorted
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
    slika = pictures[0].slika
    sommeliers = Somelijer.objects.filter(idponuda=offer.idponuda.idponuda_id)
    context = {
        'vinarija': winery,
        'obilasci': typesOfTour,
        'slika': slika,
        'somelijeri': sommeliers
    }
    return render(request, "obilazakPojedinacanPrikaz.html", context)


def makeList(list, n):
    offer = Ponuda.objects.all()
    forCnt = 0
    rowsOfCelebrations = []
    row = []
    for celebration in list:
        c = offer.filter(idponuda=celebration.idponuda_id)
        winery = Korisnik.objects.filter(email=c[0].idkorisnik)[0].javnoime
        pictures = Slika.objects.filter(idponuda=celebration.idponuda_id)
        tmp = TempProstor(winery, pictures[0].slika)
        row.append(tmp)
        if (forCnt % 3 == 0 and forCnt != 0) or (n <= 3 and forCnt == n - 1):
            rowsOfCelebrations.append(row)
            row = []
        forCnt += 1
    return rowsOfCelebrations


def celebration(request):
    celebrations = Proslava.objects.all()
    filteredCelebrations = []
    if request.method == 'POST' and request.POST.get('filter') != None:
        filter = request.POST.get('filter')
        if filter == 'Do 40 mesta':
            filteredCelebrations = celebrations.filter(kapacitet__range=(0, 40))
        elif filter == '40-80 mesta':
            filteredCelebrations = celebrations.filter(kapacitet__range=(41, 80))
        elif filter == '80-100 mesta':
            filteredCelebrations = celebrations.filter(kapacitet__range=(81, 100))
        else:
            filteredCelebrations = celebrations.filter(kapacitet__gt=100)

        if len(list(filteredCelebrations)) == 0:
            context = {
                "proslave": filteredCelebrations
            }
            return render(request, "pregledProslava.html", context)

    if len(list(filteredCelebrations)) == 0:
        rowsOfCelebrations = makeList(celebrations, len(list(celebrations)))
    else:
        rowsOfCelebrations = makeList(filteredCelebrations, len(list(filteredCelebrations)))

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
