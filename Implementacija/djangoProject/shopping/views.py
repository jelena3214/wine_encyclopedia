import os
from http.client import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from baza.models import *
from userApp.views import send_custom_email


class TempVino:
    def __init__(self, naziv, opis, cena, slika, id, kolicina):
        self.naziv = naziv
        self.cena = cena
        self.slika = slika
        self.opis = opis
        self.id = id
        self.kolicina = kolicina


@login_required(login_url='/user')
def shoppingCart(request):
    tempWines = []
    print("vala odje1")
    wines = Vino.objects.filter(ukorpi__idkorisnik=request.user)
    print(request.user.id)
    for wine in wines:
        print("vala odje")
        image = Slika.objects.get(idponuda=wine.idponuda)
        inCart = Ukorpi.objects.get(idkorisnik=request.user, idponuda=wine)
        tempWine = TempVino(wine.naziv, wine.opisvina, wine.cena, image.slika, wine.idponuda.idponuda, inCart.kolicina)
        tempWines.append(tempWine)
    context = {
        'wines': tempWines
    }
    return render(request, 'korpaZaKupovinu.html', context)


@login_required(login_url='/user')
def shoppingDone(request):
    if request.method == 'POST':
        email = request.user.email
        sumPrices = request.POST.getlist('sumPrices[]')
        # try:
        wines = Vino.objects.filter(ukorpi__idkorisnik=request.user)
        tempWines = []
        index = 0
        for wine in wines:
            image = Slika.objects.get(idponuda=wine.idponuda)
            inCart = Ukorpi.objects.get(idkorisnik=request.user, idponuda=wine)
            tempWine = TempVino(wine.naziv, wine.opisvina, wine.cena, "", sumPrices[index],
                                inCart.kolicina)
            tempWines.append((index, tempWine))
            index += 1
            wine.brojprodatih += 1
            wine.save(update_fields=['brojProdatih'])
        send_custom_email(email, 'Enciklopedija vina račun', 'racunKupovina.html',
                          {'wines': tempWines,
                           'theTotal': request.POST.get('theTotal')
                           })#context of the mail
        items = Ukorpi.objects.filter(idkorisnik=request.user)
        for item in items:
            item.delete()
    context = {
        'text': 'Čestitamo na uspešnoj kupovini!'
    }
    return render(request, 'potvrdaKupovine.html', context)


@login_required(login_url='/user')
def reservationCelebrationDone(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Korisnik.objects.get(email=email)
            send_custom_email(email, 'Enciklopedija vina račun', 'racunRezervacijaProslava.html',
                              {})#context mejla
        except Exception:
            # If user is not registered on the site we won't send the email
            return redirect(request.path)
    context = {
        'text': 'Čestitamo na uspešnoj rezervaciji!'
    }
    return render(request, 'potvrdaKupovine.html', context)


@login_required(login_url='/user')
def reservationVisitDone(request):
    if request.method == 'POST':
        email = request.user.email
        date = request.POST['date']
        print("Date " + date)
        numPeople = int(request.POST['quantity'])
        print("numPeople " + str(numPeople))
        someliers = request.POST.getlist('somelijer')
        print("num someliers " + str(len(someliers)))
        visitOptionId = request.POST.get('obilazak')
        visitOption = Vrstaobilaska.objects.get(idobilazak=visitOptionId)
        print("idPonuda " + str(visitOption.idponuda.idponuda.idponuda.idponuda))
        sumPrice = visitOption.cena * numPeople
        print("sumPrice " + str(sumPrice))
        visit = visitOption.idponuda
        print("cenaSomelijeraJednog " + str(visit.cenasomelijera))
        somelierPrice = visit.cenasomelijera * len(someliers)
        if (len(someliers)):
            print("somelijerID: " + someliers[0])
        print("cenaSomelijeraSvih " + str(somelierPrice))
        producer = visit.idponuda.idponuda.idkorisnik.proizvodjac
        print("Producer " + producer.email)
        print("NameOfTheFirm " + producer.imefirme)
        send_custom_email(email, 'Enciklopedija vina račun', 'racunRezervacijaObilazak.html',
                          {
                              'place': producer.imefirme,
                              'packageName': visitOption.naziv,
                              'packageDesc': visitOption.opis,
                              'date': date,
                              'numPeople': numPeople,
                              'price': sumPrice,
                              'someliers': someliers,
                              'somelierPrice': somelierPrice,
                              'priceTotal': sumPrice+somelierPrice
                          })#context mejla
        newRes = Termin()
        newRes.vreme = date;
        newRes.idponuda = visit.idponuda
        newRes.save()
    context = {
        'text': 'Čestitamo na uspešnoj rezervaciji!'
    }
    return render(request, 'potvrdaKupovine.html', context)


@login_required(login_url='/user')
def mejlProba(request):
    return render(request, 'emails/racunRezervacijaObilazak.html')


@login_required(login_url='/user')
def deleteItemCart(request):
    if request.method == 'POST':
        idponuda = request.POST.get('itemId')
        item = Ukorpi.objects.get(idponuda=idponuda, idkorisnik=request.user)
        item.delete()
        return JsonResponse({'result': 'Success'})


@login_required(login_url='/user')
def emptyCart(request):
    if request.method == 'POST':
        items = Ukorpi.objects.filter(idkorisnik=request.user)
        for item in items:
            print(item)
            item.delete()
    context = {
        'wines': []
    }
    return redirect('/shopping/shoppingCart')


@login_required(login_url='/user')
def addToCart(request):
    if request.method == 'POST':
        idItem = request.POST.get('idItem')
        wine = Vino.objects.get(idponuda__idponuda=idItem)
        quantity = request.POST.get('quantity')
        if Ukorpi.objects.filter(idponuda=wine, idkorisnik=request.user):
            item = Ukorpi.objects.get(idponuda=wine)
            item.kolicina += int(quantity)
            item.save(update_fields=['kolicina'])
        else:
            item = Ukorpi()
            item.idponuda = wine
            item.idkorisnik = request.user
            item.kolicina = quantity
            item.save()
    return redirect('/views/allwines')


@login_required(login_url='/user')
def changeQuantity(request):
    if request.method == 'POST':
        itemId = request.POST.get('itemId')
        wine = Vino.objects.get(idponuda__idponuda=itemId)
        newQuantity = request.POST.get('newQuantity')
        item = Ukorpi.objects.get(idponuda=wine)
        item.kolicina = int(newQuantity)
        item.save(update_fields=['kolicina'])
        return JsonResponse({'result': 'Success'})
