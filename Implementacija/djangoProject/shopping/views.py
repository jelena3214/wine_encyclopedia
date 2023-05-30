import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from baza.models import *
from userApp.views import send_custom_email
from views.views import TempVino

@login_required(login_url='/user')
def shoppingCart(request, folder_path=None, image_name=None):
    tempVines = []
    vines = Vino.objects.filter(ukorpi__idkorisnik=request.user)
    for vine in vines:
        image = Slika.objects.get(idponuda=vine.idponuda)
        imagePath = findImagePath(image.slika)
        tempVine = TempVino(vine.naziv, vine.opisvina, vine.cena, imagePath, vine.idponuda.idponuda)
        tempVines.append(tempVine)
    context = {
        'vines': tempVines
    }
    return render(request, "korpaZaKupovinu.html", context)

@login_required(login_url='/user')
def shoppingDone(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # user = Korisnik.objects.get(email=email)
            vines = Vino.objects.filter(ukorpi__idkorisnik=request.user)
            send_custom_email(email, 'Enciklopedija vina račun', 'racunKupovina.html',
                              {'vines': vines,
                               'quantities': request.POST.get('quantities'),
                               'sumPrices': request.POST.get('sumPrices'),
                               'theTotal': request.POST.get('theTotal')
                               })#context mejla

            items = Ukorpi.objects.filter(idkorisnik=request.user)
            for item in items:
                print(item)
                item.delete()
        except Exception:
            # If user is not registered on the site we won't send the email
            return redirect(request.path)
    context = {
        'text': "Čestitamo na uspešnoj kupovini!"
    }
    return render(request, "potvrdaKupovine.html", context)

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
        'text': "Čestitamo na uspešnoj rezervaciji!"
    }
    return render(request, "potvrdaKupovine.html", context)

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
        'text': "Čestitamo na uspešnoj rezervaciji!"
    }
    return render(request, "potvrdaKupovine.html", context)

@login_required(login_url='/user')
def mejlProba(request):
    return render(request, "emails/racunRezervacijaProslava.html")

@login_required(login_url='/user')
def findImagePath(imageName):
    imageFolderPath = 'static/images'
    subdirectory, imageName = imageName.split('/')
    for filename in os.listdir(imageFolderPath):
        if filename.startswith(imageName):
            imagePath = '/' + imageFolderPath + '/' + filename
    return imagePath

@login_required(login_url='/user')
def deleteItemCart(request):
    if request.method == 'POST':
        idponuda = request.POST.get('itemId')
        item = Ukorpi.objects.get(idponuda=idponuda, idkorisnik=request.user)
        item.delete()

@login_required(login_url='/user')
def emptyCart(request):
    if request.method == 'POST':
        items = Ukorpi.objects.filter(idkorisnik=request.user)
        for item in items:
            print(item)
            item.delete()
    tempVines = []
    context = {
        'vines': tempVines
    }
    return redirect("/shopping/shoppingCart")

@login_required(login_url='/user')
def addToCart(request):
    idItem = request.POST.get("idItem")
    quantity = request.POST.get("quantity")
    item = Ukorpi()
    item.idponuda = Vino.objects.get(idponuda=idItem)
    item.idkorisnik = request.user
    item.kolicina = quantity
    item.save()