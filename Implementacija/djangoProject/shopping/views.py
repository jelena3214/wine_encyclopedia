from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from baza.models import *
from userApp.views import send_custom_email

"""
    Author: Bojana Malesevic 2020/0235
    Methods for getting items from shopping cart, buying the cart contents, 
    handling reservation of celebrations and visits/detours, emptying the cart, adding items to cart.
    Handling Ajax requests for deleting items from cart or changing quantities of item instances. 
    Methods for getting questionnaire questions and results(recommended tags). 
    All the methods are passed a request, and produce html response.
"""


class TempVino:
    def __init__(self, naziv, opis, cena, slika, id, kolicina):
        # string - wine name
        self.naziv = naziv
        # int - wine price
        self.cena = cena
        # string - url of wine image
        self.slika = slika
        # string - wine description
        self.opis = opis
        # int - wine id
        self.id = id
        # int - num of instances of the wine
        self.kolicina = kolicina


#  getting items from shopping cart to view
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


#  buying the items in cart
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

        #  get some details of items from cart
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
            'text': 'Čestitamo na uspešnoj kupovini!',
            'email': email
        }
        return render(request, 'potvrdaKupovine.html', context)
    else:
        #  avoiding purchasing an empty cart
        if len(Vino.objects.filter(ukorpi__idkorisnik=request.user)) == 0:
            return redirect('/shopping/shoppingCart')
        else:
            context = {
                'text': 'Čestitamo na uspešnoj kupovini!',
                'email': request.user.email
            }
            return render(request, 'potvrdaKupovine.html', context)


#  reserve the celebration venue in the winery
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

        #  check if this winery on this date is already reserved so the producer can be notified
        similarReservExists = ''
        if Termin.objects.filter(vreme=date, idponuda=celebrationPonudaProstor):
            similarReservExists = 'Rezervacija za isti datum već postoji, molimo da proverite regularnost i javite klijentima na mejl ukoliko rezervacija nije validna.'

        #  send reservation details to both parties
        send_custom_email(email, 'Enciklopedija vina račun', 'racunRezervacijaProslava.html',
                          {
                              'winery': producer.imefirme,
                              'address': address,
                              'date': date,
                              'numPeople': numPeople,
                              'price': price,
                              'priceTotal': price * numPeople
                          })
        send_custom_email(producerUser.email, 'Enciklopedija vina rezervacija', 'rezervacijaProslavaObavestenje.html',
                          {
                              'date': date,
                              'email': email,
                              'additionalText': similarReservExists,
                              'winery': producer.imefirme,
                              'address': address,
                              'numPeople': numPeople,
                              'price': price,
                              'priceTotal': price * numPeople
                          })

        # new element in Termin
        newTerm = Termin()
        newTerm.vreme = date
        newTerm.idponuda = celebrationPonudaProstor
        newTerm.brojljudi = numPeople
        newTerm.save()
        # new element in Rezervacija
        newRes = Rezervacija()
        newRes.idtermin = newTerm
        newRes.idkorisnik = request.user
        newRes.save()

    context = {
        'text': 'Čestitamo na uspešnoj rezervaciji prostora za proslavu!',
        'email': email
    }
    return render(request, 'potvrdaKupovine.html', context)


#  reserve the visit in the winery
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
        producerUser = visit.idponuda.idponuda.idkorisnik
        producer = visit.idponuda.idponuda.idkorisnik.proizvodjac
        address = visit.idponuda.idponuda.idkorisnik.adresa

        #  check if this winery on this date is already reserved so the producer can be notified
        similarReservExists = ''
        if Termin.objects.filter(vreme=date, idponuda=visitPonudaProstor):
            similarReservExists = 'Rezervacija za isti datum već postoji, molimo da proverite regularnost i javite klijentima na mejl ukoliko rezervacija nije validna.'

        #  send reservation details to both parties
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
        send_custom_email(producerUser.email, 'Enciklopedija vina rezervacija', 'rezervacijaObilazakObavestenje.html',
                          {
                              'date': date,
                              'email': email,
                              'additionalText': similarReservExists,
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
        newTerm.brojljudi = numPeople
        newTerm.save()
        # new element in Rezervacija
        newRes = Rezervacija()
        newRes.idtermin = newTerm
        newRes.idkorisnik = request.user
        newRes.save()

    context = {
        'text': 'Čestitamo na uspešnoj rezervaciji obilaska vinarije!',
        'email': email
    }
    return render(request, 'potvrdaKupovine.html', context)


#  handles emptying the cart, deleting items
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


#  handles adding to cart a chosen number of instances
#  of the wine that is being viewed
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


#  handles Ajax request to delete an item from cart
@login_required(login_url='/user')
def deleteItemCart(request):
    if request.method == 'POST':
        idponuda = request.POST.get('itemId')
        item = Ukorpi.objects.get(idponuda=idponuda, idkorisnik=request.user)
        item.delete()
        return JsonResponse({'result': 'Success'})


#  handles Ajax request to change number of instances of a wine in cart
def changeQuantity(request):
    if request.method == 'POST':
        itemId = request.POST.get('itemId')
        newQuantity = request.POST.get('newQuantity')
        wine = Vino.objects.get(idponuda__idponuda=itemId)
        item = Ukorpi.objects.get(idponuda=wine)
        item.kolicina = int(newQuantity)
        item.save(update_fields=['kolicina'])
        return JsonResponse({'result': 'Success'})


#  gets questionnaire starting page
@login_required(login_url='/user')
def questionnaire(request):
    return render(request, 'upitnikPocetnaStrana.html')


#  gets questionnaire content to be filled out
@login_required(login_url='/user')
def questionnaireQ(request):
    questions = []
    questionsBase = Upitnikpitanje.objects.all()
    for qi in range(len(questionsBase)):
        answersBase = Upitnikodgovor.objects.filter(idpitanje=questionsBase[qi])
        answers = []
        for qa in range(len(answersBase)):
            answers.append((qa+1, answersBase[qa]))
        questions.append((qi+1, questionsBase[qi].tekst, answers))

    context = {
        'questions' : questions
    }
    return render(request, 'upitnikPitanja.html', context)


#  calculates questionnaire results based on chosen answers
@login_required(login_url='/user')
def questionnaireRes(request):
    if request.method == "POST":
        tagCount = {}
        for qi in range(len(Upitnikpitanje.objects.all())):
            tagName = request.POST.get('question' + str(qi+1))
            if tagName in tagCount:
                tagCount[tagName] += 1
            else:
                tagCount[tagName] = 1

        #  gets the tag that was chosen the most
        maxCount = max(tagCount.values())
        for tagName, count in tagCount.items():
            if count == maxCount:
                maxTagName = tagName
                break

        tagsBase = Tag.objects.filter(tag=maxTagName)
        res = Rezultatupitnika()
        res.idtag = tagsBase[0]
        res.idkorisnik = request.user
        res.save()

        context = {
            'tag': maxTagName,
            'num': len(tagsBase)
        }
        return render(request, 'upitnikRes.html', context)
    return redirect('/shopping/questionnaire')


#  gets questionnaire history of results
@login_required(login_url='/user')
def questionnaireHist(request):
    results = Rezultatupitnika.objects.filter(idkorisnik=request.user)
    tags = []
    for res in results:
        tags.append(res.idtag.tag)
    context = {
        'tags': tags
    }
    return render(request, 'upitnikIstorijaRes.html', context)
