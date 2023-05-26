from django.shortcuts import render
from baza.models import Vino
# Create your views here.




def viewWine(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        print(request.POST)
        # new_wine = Vino()
        # new_wine.naziv = request.POST['wineName']
        # new_wine.cena = request.POST['price']
        # new_wine.brojprodatih = 0
        # new_wine.opisvina = request.POST['description']
        # tags = request.POST['taginputs']
        # new_wine.idponuda = 1
        # new_wine.save()
    return render(request,"unosVina.html")


def inputTour(request):


    return render(request,"unosObilaska.html")

def addTourType(request):
    if request.method == "POST":
        print(request.POST)
    return render(request,"unosObilaska.html")

def inputTourPicture(request):
    if request.method == "POST":
        print(request.POST)
    return render(request,"unosObilaska.html")


def inputCelebration(request):

    return render(request,"unosProslave.html")


def myStore(request):
    return render(request,"mojaProdavnica.html")
