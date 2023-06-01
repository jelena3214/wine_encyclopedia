from django.shortcuts import render, redirect
from baza.models import *
from random import choice, choices


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
wnry = None


def viewWines(request):
    global sorted, filtered, wnry
    sortToDisplay = None
    wines = Vino.objects.all()
    tags = list(Tag.objects.all().values('tag').distinct())
    wineries = Proizvodjac.objects.all()
    listOfWineries = []
    for winery in wineries:
        listOfWineries.append(winery.javnoime)
    listOfTags = []
    for tag in tags:
        listOfTags.append(tag["tag"])

    rowsOfWines = []
    row = []
    filter = request.POST.get('filter')
    sort = request.POST.get('sort')
    wineryFilter = request.POST.get('winery')
    ids = []

    if filter == '':
        filtered = None

    if sort == '':
        sorted = None

    if wineryFilter == '':
        wnry = None

    if request.method == 'POST':
        offers = []
        if wineryFilter:
            wnry = wineryFilter
            ids, offers = findWinesByWinery()

        if filter:
            filtered = filter
            if len(offers) == 0:
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
            else:
                winesTags = Tag.objects.filter(tag=filter)
                filteredOffer = []
                for tag in winesTags:
                    try:
                        offer = Vino.objects.get(idponuda=tag.idponuda_id)
                    except:
                        offer = None
                    if offer in offers:
                        filteredOffer.append(offer)
                offers = filteredOffer

        if filtered is None and len(offers) == 0:
            queryset = Vino.objects.all()
            if sorted == 'Po ceni rastuce':
                queryset = queryset.order_by('cena')
                offers = list(queryset)
            elif sorted == 'Po ceni opadajuce':
                queryset = queryset.order_by('-cena')
                offers = list(queryset)
            else:
                offers = list(queryset)
        if sort:
            sorted = sort
            if sort == 'Po ceni rastuce':
                sortToDisplay = "Po ceni opadajuce"
                if filtered or wnry:
                    offers = list(Vino.objects.filter(idponuda__in=ids).order_by('cena'))
                else:
                    offers = list(Vino.objects.all().order_by('cena'))
            else:
                sortToDisplay = "Po ceni rastuce"
                if filtered or wnry:
                    offers = list(Vino.objects.filter(idponuda__in=ids).order_by('-cena'))
                else:
                    offers = list(Vino.objects.all().order_by('-cena'))
        forCnt = 0
        for wine in offers:
            pictures = Slika.objects.filter(idponuda=wine.idponuda_id)
            picture = pictures[0].slika
            tmp = TempVino(wine.naziv, wine.opisvina, wine.cena, picture, wine.idponuda_id)
            row.append(tmp)
            if (forCnt + 1) % 3 == 0 and forCnt != 0:
                rowsOfWines.append(row)
                row = []
            forCnt += 1
        if row not in rowsOfWines:
            rowsOfWines.append(row)

    else:
        filtered = None
        sorted = None
        wnry = None
        forCnt = 0
        for wine in wines:
            pictures = Slika.objects.filter(idponuda=wine.idponuda_id)
            tmp = TempVino(wine.naziv, wine.opisvina, wine.cena, pictures[0].slika, wine.idponuda_id)
            row.append(tmp)
            if (forCnt + 1) % 3 == 0:
                rowsOfWines.append(row)
                row = []
            forCnt += 1
        if row not in rowsOfWines:
            rowsOfWines.append(row)

    if filter:
        listOfTags.remove(filter)

    if wineryFilter:
        listOfWineries.remove(wineryFilter)

    context = {
        'vina': rowsOfWines,
        'tagovi': listOfTags,
        'filter': filtered,
        'sort1': sortToDisplay,
        'sort': sorted,
        'wineries': listOfWineries,
        'winery': wnry
    }

    return render(request, "pregledVina.html", context)


def findWinesByWinery():
    winery = Proizvodjac.objects.get(javnoime=wnry)

    allOffers = list(Ponuda.objects.filter(idkorisnik=winery.id))
    wines = []
    ids = []
    for offer in allOffers:
        try:
            wine = Vino.objects.get(idponuda=offer.idponuda)
        except Vino.DoesNotExist:
            wine = None
        if wine:
            wines.append(wine)
            ids.append(wine.idponuda_id)
    return ids, wines


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

    if request.method == 'POST':
        filter = request.POST.get('filter')

        if filter == 'Ima somelijera':
            filteredTours = []
            for tour in tours:
                someliers = Somelijer.objects.filter(idponuda=tour.idponuda_id)
                if len(someliers) > 0:
                    filteredTours.append(tour)
            tours = filteredTours
        elif filter == 'Nema somelijera':
            filteredTours = []
            for tour in tours:
                someliers = Somelijer.objects.filter(idponuda=tour.idponuda_id)
                if len(someliers) == 0:
                    filteredTours.append(tour)
            tours = filteredTours

    for tour in tours:
        o = offer.filter(idponuda=tour.idponuda_id)
        winery = Korisnik.objects.filter(email=o[0].idkorisnik)[0].javnoime
        picture = Slika.objects.filter(idponuda=tour.idponuda_id).first().slika
        tmp = TempProstor(winery, picture)
        row.append(tmp)
        if (forCnt + 1) % 3 == 0:
            rowsOfTours.append(row)
            row = []
        forCnt += 1
    if row not in rowsOfTours:
        rowsOfTours.append(row)

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
        if (forCnt + 1) % 3 == 0:
            rowsOfCelebrations.append(row)
            row = []
        forCnt += 1
    if row not in rowsOfCelebrations:
        rowsOfCelebrations.append(row)
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
        if (forCnt + 1) % 3 == 0:
            rowsOfWine.append(row)
            row = []
        forCnt += 1
    if row not in rowsOfWine:
        rowsOfWine.append(row)

    context = {
        "premium": premiumSubscriber,
        'one': one,
        'two': two,
        "wines": rowsOfWine
    }
    return render(request, "pocetna.html", context)
