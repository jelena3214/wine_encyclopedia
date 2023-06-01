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
    wines = Vino.objects.filter(ukorpi__idkorisnik=request.user)
    for wine in wines:
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
        wines = Vino.objects.filter(ukorpi__idkorisnik=request.user)
        tempWines = []
        index = 0
        if len(wines) == 0:
            return redirect('/shopping/shoppingCart')
        for wine in wines:
            image = Slika.objects.get(idponuda=wine.idponuda)
            inCart = Ukorpi.objects.get(idkorisnik=request.user, idponuda=wine)
            tempWine = TempVino(wine.naziv, wine.opisvina, wine.cena, "", sumPrices[index],
                                inCart.kolicina)
            tempWines.append((index, tempWine))
            index += 1
            wine.brojprodatih += inCart.kolicina
            wine.save(update_fields=['brojprodatih'])
        #  send payment infomation via email
        send_custom_email(email, 'Enciklopedija vina račun', 'racunKupovina.html',
                          {'wines': tempWines,
                           'theTotal': request.POST.get('theTotal')
                           })
        #  clear the cart
        items = Ukorpi.objects.filter(idkorisnik=request.user)
        for item in items:
            item.delete()
        context = {
            'text': 'Čestitamo na uspešnoj kupovini!'
        }
        return render(request, 'potvrdaKupovine.html', context)
    else:
        #  avoiding purchasing an empty cart
        if len(Vino.objects.filter(ukorpi__idkorisnik=request.user)) == 0:
            return redirect('/shopping/shoppingCart')
        else:
            context = {
                'text': 'Čestitamo na uspešnoj kupovini!'
            }
            return render(request, 'potvrdaKupovine.html', context)


@login_required(login_url='/user')
def reservationCelebrationDone(request):
    if request.method == 'POST':
        email = request.user.email
        date = request.POST['date']
        numPeople = int(request.POST['quantity'])
        price = int(request.POST.get('price'))
        celebrationId = request.POST.get('celebrationId')
        celebrationPonuda = Ponuda.objects.get(idponuda=celebrationId)
        celebrationPonudaProstor = Ponudaprostor.objects.get(idponuda=celebrationPonuda)
        producerUser = celebrationPonuda.idkorisnik
        address = producerUser.adresa
        producer = producerUser.proizvodjac
        send_custom_email(email, 'Enciklopedija vina račun', 'racunRezervacijaProslava.html',
                          {
                              'winery': producer.imefirme,
                              'address': address,
                              'date': date,
                              'numPeople': numPeople,
                              'price': price,
                              'priceTotal': price * numPeople
                          })
        # new element in Termin
        newTerm = Termin()
        newTerm.vreme = date
        newTerm.idponuda = celebrationPonudaProstor
        newTerm.save()
        # new element in Rezervacija
        newRes = Rezervacija()
        newRes.idtermin = newTerm
        newRes.idkorisnik = request.user
        newRes.save()

    context = {
        'text': 'Čestitamo na uspešnoj rezervaciji prostora za proslavu!'
    }
    return render(request, 'potvrdaKupovine.html', context)


@login_required(login_url='/user')
def reservationVisitDone(request):
    if request.method == 'POST':
        email = request.user.email
        date = request.POST['date']
        numPeople = int(request.POST['quantity'])
        sommelierNames = request.POST.getlist('somelijer')
        visitOptionId = request.POST.get('obilazak')
        visitOption = Vrstaobilaska.objects.get(idobilazak=visitOptionId)
        price = visitOption.cena
        visit = visitOption.idponuda
        visitPonudaProstor = visit.idponuda
        sommelierPrice = visit.cenasomelijera * len(sommelierNames)
        producer = visit.idponuda.idponuda.idkorisnik.proizvodjac
        address = visit.idponuda.idponuda.idkorisnik.adresa
        send_custom_email(email, 'Enciklopedija vina račun', 'racunRezervacijaObilazak.html',
                          {
                              'winery': producer.imefirme,
                              'address': address,
                              'packageName': visitOption.naziv,
                              'packageDesc': visitOption.opis,
                              'date': date,
                              'numPeople': numPeople,
                              'price': price,
                              'sommelierNames': sommelierNames,
                              'sommelierPrice': sommelierPrice,
                              'priceTotal': price * numPeople + sommelierPrice
                          })
        # new element in Termin
        newTerm = Termin()
        newTerm.vreme = date
        newTerm.idponuda = visitPonudaProstor
        newTerm.save()
        # new element in Rezervacija
        newRes = Rezervacija()
        newRes.idtermin = newTerm
        newRes.idkorisnik = request.user
        newRes.save()
    context = {
        'text': 'Čestitamo na uspešnoj rezervaciji obilaska vinarije!'
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
            item.delete()
    context = {
        'wines': []
    }
    return redirect('/shopping/shoppingCart')


@login_required(login_url='/user')
def addToCart(request):
    if request.method == 'POST':
        idItem = request.POST.get('idItem')
        quantity = request.POST.get('quantity')
        wine = Vino.objects.get(idponuda__idponuda=idItem)
        #  wine already in cart
        if Ukorpi.objects.filter(idponuda=wine, idkorisnik=request.user):
            item = Ukorpi.objects.get(idponuda=wine)
            item.kolicina += int(quantity)
            item.save(update_fields=['kolicina'])
        #  wine new in cart
        else:
            item = Ukorpi()
            item.idponuda = wine
            item.idkorisnik = request.user
            item.kolicina = quantity
            item.save()
    return redirect('/views/allwines')


def changeQuantity(request):
    if request.method == 'POST':
        itemId = request.POST.get('itemId')
        newQuantity = request.POST.get('newQuantity')
        wine = Vino.objects.get(idponuda__idponuda=itemId)
        item = Ukorpi.objects.get(idponuda=wine)
        item.kolicina = int(newQuantity)
        item.save(update_fields=['kolicina'])
        return JsonResponse({'result': 'Success'})
