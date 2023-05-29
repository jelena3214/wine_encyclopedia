import fnmatch
import os

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


class TempProstor:
    def __init__(self, ime, slika):
        self.ime = ime
        self.slika = slika


class TempProslava:
    def __init__(self, ime, slika, id):
        self.ime = ime
        self.slika = slika # niz slika
        self.id = id


def viewWines(request):
    vina = Vino.objects.all()
    print(vina)
    tagovi = list(Tag.objects.all().values('tag').distinct())
    tags = []
    for tag in tagovi:
        tags.append(tag["tag"])
    vinaRedovi = []
    vinoRed = []

    if request.method == 'POST' and request.POST.get('filter') != None:
        filter = request.POST.get('filter')
        tagovi = Tag.objects.filter(tag=filter)
        ponude = []
        for tag in tagovi:
            ponuda = Vino.objects.filter(idponuda=tag.idponuda_id).first()
            ponude.append(ponuda)

        forCnt = 0
        for vino in ponude:
            slike = Slika.objects.filter(idponuda=vino.idponuda_id)
            tmp = TempVino(vino.naziv, vino.opisvina, vino.cena, slike[0].slika, vino.idponuda_id)
            vinoRed.append(tmp)
            if (forCnt % 3 == 0 and forCnt != 0) or (len(ponude) <= 3 and forCnt == len(ponude) - 1):
                vinaRedovi.append(vinoRed)
                vinoRed = []
            forCnt += 1
    else:
        forCnt = 0
        for vino in vina:
            slike = Slika.objects.filter(idponuda=vino.idponuda_id)
            tmp = TempVino(vino.naziv, vino.opisvina, vino.cena, slike[0].slika, vino.idponuda_id)
            vinoRed.append(tmp)
            if forCnt % 3 == 0 and forCnt != 0 or (len(vina) <= 3 and forCnt == len(vina) - 1):
                vinaRedovi.append(vinoRed)
                vinoRed = []
            forCnt += 1

    context = {
        'vina': vinaRedovi,
        'tagovi': tags
    }

    return render(request, "pregledVina.html", context)


def wine(request, value):
    @login_required
    def recenzija(request, id):
        ocena = request.POST.get('rate')
        korisnik = request.user
        tekst = request.POST.get('recenzija')
        novaRec = Recenzija(idponuda=Ponuda(idponuda=id, idkorisnik_id=korisnik), idkorisnik_id=korisnik.id,
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
        vinarija = Korisnik.objects.filter(email=o[0].idkorisnik)[0].javnoime
        sl = Slika.objects.filter(idponuda=obilazak.idponuda_id)[0].slika
        tmp = TempProstor(vinarija, sl)
        obilazakRed.append(tmp)
        if (forCnt % 3 == 0 and forCnt != 0) or (len(obilasci) <= 3 and forCnt == len(obilasci) - 1):
            obilazakRedovi.append(obilazakRed)
            obilazakRed = []
        forCnt += 1

    context = {
        'obilasci': obilazakRedovi
    }

    return render(request, "pregledObilazaka.html", context)


def oneDetour(request, value):
    ime = value[1:]
    korisnici = Korisnik.objects.filter(javnoime=ime)
    vinarija = None
    for korisnik in korisnici:
        pr = Proizvodjac.objects.filter(email=korisnik.email)
        if pr is not None:
            vinarija = pr[0]
            break
    ponude = Ponuda.objects.filter(idkorisnik_id=vinarija.id)
    ponuda = None
    obilasci = Obilazak.objects.all()
    for p in ponude:
        pr = obilasci.filter(idponuda=p.idponuda)
        if len(pr):
            ponuda = pr[0]
    if ponuda is None:
        return celebration(request)

    vrsteobilazaka = Vrstaobilaska.objects.filter(idponuda=ponuda.idponuda.idponuda_id)
    slike = Slika.objects.filter(idponuda=ponuda.idponuda.idponuda_id)
    somelijeri = Somelijer.objects.filter(idponuda=ponuda.idponuda.idponuda_id)
    context = {
        'vinarija' : vinarija,
        'obilasci': vrsteobilazaka,
        'slika': slike[0],
        'somelijeri': somelijeri
    }
    return render(request, "obilazakPojedinacanPrikaz.html", context)


def celebration(request):
    ponuda = Ponuda.objects.all()
    proslave = Proslava.objects.all()
    proslavaRedovi = []
    proslavaRed = []
    forCnt = 0

    for proslava in proslave:
        p = ponuda.filter(idponuda=proslava.idponuda_id)
        vinarija = Korisnik.objects.filter(email=p[0].idkorisnik)[0].javnoime
        slike = Slika.objects.filter(idponuda=proslava.idponuda_id)
        tmp = TempProstor(vinarija, slike[0].slika)
        proslavaRed.append(tmp)
        if (forCnt % 3 == 0 and forCnt != 0) or (len(proslave) <= 3 and forCnt == len(proslave) - 1):
            proslavaRedovi.append(proslavaRed)
            proslavaRed = []
        forCnt += 1

    context = {
        'proslave': proslavaRedovi
    }

    return render(request, "pregledProslava.html", context)


def oneCelebration(request, value):
    ime = value[1:]
    korisnici = Korisnik.objects.filter(javnoime=ime)
    vinarija = None
    for korisnik in korisnici:
        pr = Proizvodjac.objects.filter(email=korisnik.email)
        if pr is not None:
            vinarija = pr[0]
            break
    ponude = Ponuda.objects.filter(idkorisnik_id=vinarija.id)
    ponuda = None
    proslave = Proslava.objects.all()
    for p in ponude:
        pr = proslave.filter(idponuda=p.idponuda)
        if len(pr):
            ponuda = pr[0]
    if ponuda is None:
        return celebration(request)

    sl = Slika.objects.filter(idponuda=ponuda.idponuda.idponuda_id)
    slike = []
    for s in sl:
        slike.append(s.slika)

    context = {
        'vinarija': vinarija,
        'slike': slike,
        'ponuda': ponuda
    }

    print(slike)
    return render(request, "proslavaPojedinacanPrikaz.html", context)


def home(request):
    return render(request, "pocetna.html")