from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from baza.models import *


class TempVino:
    def __init__(self, naziv,opis, cena, slika, id):
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


class TempObilazak:
    def __init__(self, ime, slika):
        self.ime = ime
        self.slika = slika


def viewWines(request):
    vina = Vino.objects.all()

    vinaRedovi = []
    vinoRed = []

    forCnt = 0
    for vino in vina:
        slike = Slika.objects.filter(idponuda=vino.idponuda_id)
        tmp = TempVino(vino.naziv, vino.opisvina, vino.cena, slike[0].slika, vino.idponuda_id)
        vinoRed.append(tmp)
        if forCnt % 3 == 0 and forCnt != 0:
            vinaRedovi.append(vinoRed)
            vinoRed = []
        forCnt += 1

    context = {
        'vina': vinaRedovi,
    }

    return render(request, "pregledVina.html", context)


def wine(request, value):
    @login_required
    def recenzija(request, id):
        ocena = request.POST.get('rate')
        korisnik = request.user
        tekst = request.POST.get('recenzija')

        novaRec = Recenzija(idrecenzija=3, idponuda=Ponuda(idponuda=id, idkorisnik_id=korisnik), idkorisnik_id=korisnik,
                            opisrec=tekst, ocena=ocena)
        novaRec.save()

    id = int(value[1:])
    if request.method == 'POST':
        recenzija(request, id)
    vino = Vino.objects.filter(idponuda=id)
    tmp = None
    tagovi = []
    recenzije = []
    if vino:
        vino = vino[0]
        slike = Slika.objects.filter(idponuda=id)
        tag = Tag.objects.filter(idponuda=id)
        rec = Recenzija.objects.filter(idponuda=id)
        if rec:
            for r in rec:
                ocena = []
                korisnik = Korisnik.objects.filter(id=r.idkorisnik_id)
                if korisnik != None:
                    for i in range(r.ocena):
                        ocena.append("+")
                    recenzije.append(TempRecenzija(r.opisrec, ocena, korisnik[0].javnoime))
        if tag:
            for t in tag:
                tagovi.append(t.tag)
        if len(slike) != 0:
            tmp = TempVino(vino.naziv.capitalize(), vino.opisvina, vino.cena, slike[0].slika, vino.idponuda_id)

    context = {
        'vino': tmp,
        'tag': tagovi,
        'recenzije': recenzije,
    }
    return render(request, "vinoPojedinacanPrikaz.html", context)


def detour(request):
    ponuda = Ponuda.objects.all()
    obilasci = Obilazak.objects.all()
    obilazakRedovi = []
    obilazakRed = []
    forCnt = 0

    for obilazak in obilasci:
        o = ponuda.filter(idponuda=obilazak.idponuda_id)
        print(o)
        vinarija = Korisnik.objects.filter(email=o[0].idkorisnik)[0].javnoime
        print(vinarija)
        slika = Slika.objects.filter(idponuda=obilazak.idponuda_id)[0].slika
        print(slika)
        tmp = TempObilazak(vinarija, slika)
        obilazakRed.append(tmp)
        if (forCnt % 3 == 0 and forCnt != 0) or (len(obilasci) < 3 and forCnt == len(obilasci) - 1):
            print("if")
            obilazakRedovi.append(obilazakRed)
            obilazakRed = []
        forCnt += 1

    print(obilazakRedovi)

    context = {
        'obilasci': obilazakRedovi
    }

    return render(request, "pregledObilazaka.html", context)


def oneDetour(request, value):
    return render(request, "obilazakPojedinacanPrikaz.html")


def celebration(request):
    return render(request, "proslavaPojedinacanPrikaz.html")


def home(request):
    return render(request, "pocetna.html")