from django.shortcuts import render


def viewWines(request):
    return render(request, "pregledVina.html")


def wine(request):
    return render(request, "vinoPojedinacanPrikaz.html")


def detour(request):
    return render(request, "obilazakPojedinacanPrikaz.html")


def celebration(request):
    return render(request, "proslavaPojedinacanPrikaz.html")


def home(request):
    return render(request, "pocetna.html")