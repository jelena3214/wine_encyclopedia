from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from baza.models import *


def registerUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if Korisnik.objects.filter(email=email).count() > 0:
            messages.error(request, message="Već postoji nalog sa unetom email adresom")
            return render(request, 'registracijaKupac.html')

        password = request.POST.get('password')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        phoneNumber = request.POST.get('phoneNumber')
        address = request.POST.get('address')
        birthDate = request.POST.get('birthDate')

        newBuyer = Kupac.objects.create_user(password=password, first_name=firstName, last_name=lastName,
                                             brtelefona=phoneNumber, adresa=address,
                                             javnoime=firstName + " " + lastName, datumrodjenja=birthDate, email=email)
        newBuyer.save()

        return redirect("loginUser")

    return render(request, 'registracijaKupac.html')


def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, message="Pogresna lozinka ili email adresa")
    return render(request, "login.html")
