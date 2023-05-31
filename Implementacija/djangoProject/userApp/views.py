import email
import os
import random
import string
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages

from baza.models import *
from .decorators import *


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
        myGroup = Group.objects.get(name='Kupci')
        myGroup.user_set.add(newBuyer)
        newBuyer.save()

        return redirect("loginUser")

    return render(request, 'registracijaKupac.html')


def registerProducer(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if Korisnik.objects.filter(email=email).count() > 0:
            messages.error(request, message="Već postoji nalog sa unetom email adresom")
            return render(request, 'registracijaProizvodjac.html')

        password = request.POST.get('password')
        name = request.POST.get('name')
        companyNumber = request.POST.get('companyNumber')

        if Proizvodjac.objects.filter(registarskibroj=companyNumber).count() > 0:
            messages.error(request, message="Već postoji vinarija sa unetim registarskim brojem")
            return render(request, 'registracijaProizvodjac.html')

        phoneNumber = request.POST.get('phoneNumber')
        address = request.POST.get('address')
        description = request.POST.get('description')
        photo = request.FILES['logo']

        newProducer = Proizvodjac.objects.create_user(password=password, imefirme=name, registarskibroj=companyNumber,
                                                      brtelefona=phoneNumber, adresa=address, opis=description,
                                                      javnoime=name, email=email, logo=photo)

        myGroup = Group.objects.get(name='Proizvodjaci')
        myGroup.user_set.add(newProducer)
        newProducer.save()

        return redirect("loginUser")

    return render(request, 'registracijaProizvodjac.html')


# User that is already logged in can't go to login page again.
# User has to log out first.
@notLoggedIn()
def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            print(request.session)
            return redirect("home")
        else:
            messages.error(request, message="Pogresna lozinka ili email adresa")
    return render(request, "login.html")


@login_required(login_url='/user')
def logoutUser(request):
    logout(request)
    return redirect("home")


@login_required(login_url='/user')
@group_required("Proizvodjaci")
def changeCompanyStuff(request):
    if request.method == "POST":
        opis = request.POST.get("opis")
        naziv = request.POST.get("naziv")
        producer = Proizvodjac.objects.get(email=request.user)

        try:
            newLogo = request.FILES['logo']
            # Delete previously uploaded logo image
            if os.path.exists(producer.logo.path):
                os.remove(producer.logo.path)
            producer.logo = newLogo
        except Exception:
            pass

        if len(opis) > 0:
            producer.opis = opis
        if len(naziv) > 0:
            producer.imefirme = naziv
            producer.javnoime = naziv
        producer.save()

        context = {
            'name': producer.imefirme,
            'description': producer.opis
        }
        return render(request, "promenaInformacijaVinarije.html", context)
    else:
        producer = Proizvodjac.objects.get(email=request.user)
        context = {
            'name': producer.imefirme,
            'description': producer.opis
        }
        return render(request, "promenaInformacijaVinarije.html", context)


@login_required(login_url='/user')
def changeInfoUser(request):
    if request.method == "POST":
        user = Korisnik.objects.get(email=request.user)
        showName = request.POST.get("showName")
        address = request.POST.get("address")
        phoneNumber = request.POST.get("phoneNumber")
        currentPassword = request.POST.get("currentPassword")
        newPassword = request.POST.get("newPassword")
        newPasswordSubmit = request.POST.get("newPasswordSubmit")

        context = {
            'showName': user.javnoime,
            'address': user.adresa,
            'phoneNumber': user.brtelefona
        }

        if len(newPassword) > 0 and not user.check_password(currentPassword):
            messages.error(request, message="Lozinka se ne poklapa sa trenutnom lozinkom naloga")
            return render(request, 'promenaInformacijaKorisnika.html', context)

        if len(newPassword) > 0 and newPassword != newPasswordSubmit:
            messages.error(request, message="Nova lozinka se nije potvrđena")
            return render(request, 'promenaInformacijaKorisnika.html', context)

        if len(newPassword) > 0 and len(newPasswordSubmit) > 0:
            user.set_password(newPassword)
        if len(showName) > 0:
            user.javnoime = showName
        if len(address) > 0:
            user.adresa = address
        if len(phoneNumber) > 0:
            user.brtelefona = phoneNumber
        user.save()

        context = {
            'showName': user.javnoime,
            'address': user.adresa,
            'phoneNumber': user.brtelefona
        }

        return render(request, 'promenaInformacijaKorisnika.html', context)
    else:
        user = Korisnik.objects.get(email=request.user)
        context = {
            'showName': user.javnoime,
            'address': user.adresa,
            'phoneNumber': user.brtelefona
        }
        return render(request, 'promenaInformacijaKorisnika.html', context)


def generate_random_password():
    length = 8
    characters = string.ascii_letters + string.digits + string.punctuation

    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        if any(c.islower() for c in password) and any(c.isupper() for c in password) and any(
                c.isdigit() for c in password):
            return password


def send_custom_email(email, subject, template_name, context):
    html_message = render_to_string('emails/' + template_name, context)
    send_mail(subject, '', 'enciklopedijavina@gmail.com', [email], html_message=html_message)


def resetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Korisnik.objects.get(email=email)
            newPass = generate_random_password()
            user.set_password(newPass)
            user.save()
            send_custom_email(email, 'Enciklopedija vina zaboravljena lozinka', 'resetovanjeLozinkeEmail.html',
                              {'newPass': newPass})
            return redirect('home')
        except Exception:
            # If user is not registered on the site we won't send the email
            return render(request, 'resetovanjeLozinke.html')
    return render(request, 'resetovanjeLozinke.html')


def userExists(request, email):
    try:
        Korisnik.objects.get(email=email)
        result = True
    except Exception:
        result = False
    return JsonResponse({'result': result})
