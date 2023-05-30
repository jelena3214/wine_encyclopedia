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


def findImagePath(imageName):
    imageFolderPath = 'static/images'
    subdirectory, imageName = imageName.split('/')
    for filename in os.listdir(imageFolderPath):
        if filename.startswith(imageName):
            imagePath = '/' + imageFolderPath + '/' + filename
    return imagePath


@login_required(login_url='/user')
def shoppingCart(request, folder_path=None, image_name=None):
    tempWines = []
    wines = Vino.objects.filter(ukorpi__idkorisnik=request.user)
    for wine in wines:
        image = Slika.objects.get(idponuda=wine.idponuda)
        imagePath = findImagePath(image.slika)
        inCart = Ukorpi.objects.get(idkorisnik=request.user, idponuda=wine)
        tempWine = TempVino(wine.naziv, wine.opisvina, wine.cena, imagePath, wine.idponuda.idponuda, inCart.kolicina)
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
            imagePath = findImagePath(image.slika)
            inCart = Ukorpi.objects.get(idkorisnik=request.user, idponuda=wine)
            tempWine = TempVino(wine.naziv, wine.opisvina, wine.cena, "", sumPrices[index],
                                inCart.kolicina)
            tempWines.append((index, tempWine))
            index += 1
        send_custom_email(email, 'Enciklopedija vina račun', 'racunKupovina.html',
                          {'wines': tempWines,
                           'theTotal': request.POST.get('theTotal')
                           })#context of the mail
        items = Ukorpi.objects.filter(idkorisnik=request.user)
        for item in items:
            print(item)
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
        email = request.POST.get('email')
        try:
            user = Korisnik.objects.get(email=email)
            send_custom_email(email, 'Enciklopedija vina račun', 'racunRezervacijaObilazak.html',
                              {})#context mejla
        except Exception:
            # If user is not registered on the site we won't send the email
            return redirect(request.path)
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
        if Ukorpi.objects.filter(idponuda=wine):
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
        print("IDITEM " + itemId)
        wine = Vino.objects.get(idponuda__idponuda=itemId)
        newQuantity = request.POST.get('newQuantity')
        item = Ukorpi.objects.get(idponuda=wine)
        item.kolicina = int(newQuantity)
        item.save(update_fields=['kolicina'])
        return JsonResponse({'result': 'Success'})
