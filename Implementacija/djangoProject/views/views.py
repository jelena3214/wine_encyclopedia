from django.shortcuts import render, redirect
from baza.models import Korisnik, Proizvodjac, Ponuda, Vino, Slika, Tag, Recenzija, Kupac


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

def viewWines(request):
    ponuda = Ponuda.objects.all()
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
    id = int(value[1:])
    if request.method == 'POST':
        ocena = request.POST.get('rate')
        korisnik = Korisnik.objects.filter(id=2)
        tekst = request.POST.get('recenzija')
        print(tekst)
        novaRec = Recenzija(idrecenzija=3,idponuda=Ponuda(idponuda=id, idkorisnik_id=2), idkorisnik_id=2, opisrec=tekst, ocena=ocena)
        novaRec.save()

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
    return render(request, "obilazakPojedinacanPrikaz.html")


def celebration(request):
    return render(request, "proslavaPojedinacanPrikaz.html")


def home(request):
    return render(request, "pocetna.html")