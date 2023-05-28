from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from baza.models import Korisnik
from userApp.views import send_custom_email


def shoppingCart(request):
    return render(request, "korpaZaKupovinu.html")

def shoppingDone(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Korisnik.objects.get(email=email)
            send_custom_email(email, 'Enciklopedija vina račun', 'racunKupovina.html',
                              {})#context mejla
        except Exception:
            # If user is not registered on the site we won't send the email
            return redirect(request.path)
    context = {
        'tekst': "Čestitamo na uspešnoj kupovini!"
    }
    return render(request, "potvrdaKupovine.html", context)

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
        'tekst': "Čestitamo na uspešnoj rezervaciji!"
    }
    return render(request, "potvrdaKupovine.html", context)

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
        'tekst': "Čestitamo na uspešnoj rezervaciji!"
    }
    return render(request, "potvrdaKupovine.html", context)

def mejlProba(request):
    return render(request, "emails/racunRezervacijaProslava.html")