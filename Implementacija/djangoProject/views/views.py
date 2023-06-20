"""
    Jovana Mitić 2020/0315
    In this file are all functions that are used for views of offers as well as function for home page
    All the methods are passed a request, and produce html response.
    All classes that are defined in this file are used for encapsulating data that is need in order to display
    all offers
"""
import datetime
from datetime import date
from django.utils import timezone
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


filtered = None # global variable that is used to check if offers should be filtered
sorted = None # global variable that is used to check if wines should be sorted
wnry = None # global variable that is used to check if wines should be filtered by winery


# function used to render page where all wines are displayed
# this function is also responsible for filtering and sorting of wines, by users request
def viewWines(request):
    global sorted, filtered, wnry
    sortToDisplay = None
    # all wines
    wines = Vino.objects.all()
    # all tags that exist in database, by which wines can be filtered
    tags = list(Tag.objects.all().values('tag').distinct())
    wineries = Proizvodjac.objects.all()
    listOfWineries = []
    # names of all wineries, by which wines can be filteres
    for winery in wineries:
        listOfWineries.append(winery.javnoime)
    listOfTags = []
    # list in which only tags are stored
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

        # filtering wines
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
        # sorting the wines, checking if they were already filtered
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
        # collecting all the necessary data for displaying the wines
        # also packing wines in rows of three or less
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
        # just displaying wines, no sorting or filtering
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


# temporary function which filters wines by winery
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



# displaying only one wine which was chosen by customer, value that is nest to request is id of wine which is chosen
# in this function reviews are also displayed and left
def wine(request, value):
    id = int(value[1:])
    star = 0
    if request.method == 'POST' and request.user.is_authenticated:
        # leaving new review if user is logged in
        mark = request.POST.get('rate')
        user = request.user
        text = request.POST.get('recenzija')
        if mark is None:
            return redirect("/views/wine/" + value)
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
            stars = 0
            for r in review:
                stars += r.ocena
                ocena = []
                user = Korisnik.objects.filter(id=r.idkorisnik_id)
                if user != None:
                    for i in range(r.ocena):
                        ocena.append("+")
                    reviews.append(TempRecenzija(r.opisrec, ocena, user[0].javnoime))
            star = int(stars / len(review))
            print(star)
        numOfStars = []
        for i in range(star):
            numOfStars.append('a')
        if tag:
            for t in tag:
                tags.append(t.tag)
        if len(pictures) != 0:
            tmp = TempVino(wine.naziv.capitalize(), wine.opisvina, wine.cena, pictures[0].slika, wine.idponuda_id)

    context = {
        'vino': tmp,
        'tag': tags,
        'recenzije': reviews,
        'zvezda': star,
        'numbers': numOfStars
    }
    return render(request, "vinoPojedinacanPrikaz.html", context)

# function used for displaying all tours that exist
# the logic is same as logic used in functin viewWines
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


# function used to display certain tour that customer wanted to see
# value is name of the winery that offers the tour
# logic used is same as the one in function wine
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
    pics = Slika.objects.filter(idponuda=offer.idponuda.idponuda_id)
    pictures = []
    for pic in pics:
        pictures.append(pic.slika)
    sommeliers = Somelijer.objects.filter(idponuda=offer.idponuda.idponuda_id)
    context = {
        'vinarija': winery,
        'obilasci': typesOfTour,
        'slike': pictures,
        'somelijeri': sommeliers
    }
    return render(request, "obilazakPojedinacanPrikaz.html", context)


# temporary function that helps with packing celebrations in rows of three or less
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


# function used to display all celebrations
# logic is same as the one used in functions detour and viewWines
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


# function used to display certain celebration that customer chose
# value is name of the winery that offers celebration
# logic is same as the one used in functions oneDetour and wine
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


# function used for displaying offers of wineries that have subscribed to one of the subscriptions that are available
# for winery that is displayed, one is chosen form premium subcribers everytime that you open or refresh the page
# for wines, if there is more, six wineries are chosen from the basic subscribers, and then random wine from their offer
# is chosen to be displatyed
# logic for showing wines is same as the logic used in functions viewWines, detour and celebration
def home(request):
    changeDates()
    subscribedBasicYearly = Pretplacen.objects.filter(idpretplata=1).filter(trenutnistatus='Aktivna')
    subscribedBasicMonthly = Pretplacen.objects.filter(idpretplata=3).filter(trenutnistatus='Aktivna')
    subscribedBasic = []
    for sub in subscribedBasicYearly:
        subscribedBasic.append(Korisnik.objects.get(id=sub.idkorisnik_id))
    for sub in subscribedBasicMonthly:
        subscribedBasic.append(Korisnik.objects.get(id=sub.idkorisnik_id))

    subscribedPremiumYearly = Pretplacen.objects.filter(idpretplata=2).filter(trenutnistatus='Aktivna')
    subscribedPremiumMonthly = Pretplacen.objects.filter(idpretplata=4).filter(trenutnistatus='Aktivna')
    subscribedPremium = []
    for sub in subscribedPremiumYearly:
        subscribedPremium.append(Korisnik.objects.get(id=sub.idkorisnik_id))
    for sub in subscribedPremiumMonthly:
        subscribedPremium.append(Korisnik.objects.get(id=sub.idkorisnik_id))

    basicSubscribers = []
    if len(list(subscribedBasic)) > 6:
        basicSubscribers = choices(list(subscribedBasic), k=6)
    else:
        basicSubscribers = list(subscribedBasic)

    if len(list(subscribedPremium)) == 0:
        allProducers = Proizvodjac.objects.all()
        premiumSubscriber = choice(list(allProducers))
    else:
        premiumSubscriber = choice(list(subscribedPremium))
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
        # print(wine.idponuda_id)
        row.append(tmp)
        if (forCnt + 1) % 3 == 0:
            rowsOfWine.append(row)
            row = []
        forCnt += 1
    if row not in rowsOfWine:
        rowsOfWine.append(row)

    if len(winesToShow) == 0:
        rowsOfWine = None
    context = {
        "premium": premiumSubscriber,
        'one': one,
        'two': two,
        "wines": rowsOfWine
    }
    return render(request, "pocetna.html", context)


def changeDates():
    subcscribed = Pretplacen.objects.all()
    for sub in subcscribed:
        if sub.datumkraj < timezone.now():
            sub.trenutnistatus = 'Istekla'
            sub.save()
        else:
            sub.trenutnistatus = 'Aktivna'
            sub.save()
