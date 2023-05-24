from django.shortcuts import render
from baza.models import Korisnik, Proizvodjac, Ponuda, Vino, Slika


class TempVino:
    def __init__(self, naziv,opis, cena, slika):
        self.naziv = naziv
        self.cena = cena
        self.slika = slika
        self.opis = opis


def viewWines(request):
    ponuda = Ponuda.objects.all()
    vina = Vino.objects.all()

    vinaRedovi = []
    vinoRed = []

    forCnt = 0
    for vino in vina:
        slike = Slika.objects.filter(idponuda=vino.idponuda_id)
        tmp = TempVino(vino.naziv, vino.opisvina, vino.cena, slike[0].slika)
        vinoRed.append(tmp)
        print(vino)
        if forCnt % 3 == 0:
            vinaRedovi.append(vinoRed)
            vinoRed = []
        forCnt += 1

    context = {
        'vina': vinaRedovi,
    }

    print(vinaRedovi)
    return render(request, "pregledVina.html", context)


def wine(request):
    return render(request, "vinoPojedinacanPrikaz.html")


def detour(request):
    return render(request, "obilazakPojedinacanPrikaz.html")


def celebration(request):
    return render(request, "proslavaPojedinacanPrikaz.html")


def home(request):
    return render(request, "pocetna.html")