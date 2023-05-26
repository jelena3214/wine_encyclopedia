import datetime
from datetime import date, datetime

from django.contrib.auth.models import Group

from baza.models import *


def init():
    groups = []
    groups.append(Group(name="Kupci"))
    groups.append(Group(name="Proizvodjaci"))
    [x.save() for x in groups]

    producers = []
    producerGroup = Group.objects.get(name='Proizvodjaci')
    p1 = Proizvodjac.objects.create_user(password="Vinarijakis123", imefirme="Vinarija Kis", registarskibroj=1234,
                                         brtelefona="+381645565656", adresa="Bulevar Oslobodjenja 67, Novi Sad",
                                         opis="Mala porodicna vinarija puna ljubavi",
                                         javnoime="Vinarija Kis", email="vinarijaKis@gmail.com")

    producerGroup.user_set.add(p1)
    p2 = Proizvodjac.objects.create_user(password="Vinarijabogdan123", imefirme="Vinarija Zvonko Bogdan",
                                         registarskibroj=1237,
                                         brtelefona="+381645565690", adresa="Palicko jezero",
                                         opis="Dodjite da pijemo zajedno i veselimo se!",
                                         javnoime="Zvonko Bogdan", email="zvonkoBogdan@gmail.com")
    producerGroup.user_set.add(p2)

    p3 = Proizvodjac.objects.create_user(password="Novasansa123", imefirme="Vinarija Nova Sansa", registarskibroj=1277,
                                         brtelefona="+381645589690", adresa="Kragujevac",
                                         opis="Porodicna vinarija",
                                         javnoime="Nova Sansa", email="novaSansa@gmail.com")
    producerGroup.user_set.add(p3)
    producers.append(p1)
    producers.append(p2)
    producers.append(p3)
    [x.save() for x in producers]

    buyers = []
    buyersGroup = Group.objects.get(name='Kupci')
    b1 = Kupac.objects.create_user(password="Jovana1234", first_name="Jovana", last_name="Mitic",
                                   brtelefona="+3817887877", adresa="Negde daleko",
                                   javnoime="Jovana Mitic", datumrodjenja=datetime(year=2002, month=1, day=16),
                                   email="jovanamitic@gmail.com")

    buyersGroup.user_set.add(b1)
    b2 = Kupac.objects.create_user(password="Bojana1234", first_name="Bojana", last_name="Malesevic",
                                   brtelefona="+3878887877", adresa="Despotovac",
                                   javnoime="Bojana Malesevic", datumrodjenja=datetime(year=2001, month=7, day=5),
                                   email="bojanamalesevic@gmail.com")
    buyersGroup.user_set.add(b2)

    b3 = Kupac.objects.create_user(password="Aleksa1234", first_name="Aleksa", last_name="Boricic",
                                   brtelefona="+3817866577", adresa="Novi Beograd",
                                   javnoime="Aleksa Boricic", datumrodjenja=datetime(year=2001, month=1, day=26),
                                   email="aleksaboricic@gmail.com")
    buyersGroup.user_set.add(b3)

    b4 = Kupac.objects.create_user(password="Jelena1234", first_name="Jelena", last_name="Cvetic",
                                   brtelefona="+3817943577", adresa="Guncati",
                                   javnoime="Jelena Cvetic", datumrodjenja=datetime(year=2001, month=3, day=26),
                                   email="jelenacvetic@gmail.com")
    buyersGroup.user_set.add(b4)
    buyers.append(b1)
    buyers.append(b2)
    buyers.append(b3)
    buyers.append(b4)
    [x.save() for x in buyers]

    offers = []
    o1 = Ponuda(idkorisnik=p1)
    o2 = Ponuda(idkorisnik=p1)
    o3 = Ponuda(idkorisnik=p1)
    o1 = Ponuda(idkorisnik=p1)
    o2 = Ponuda(idkorisnik=p1)
    o3 = Ponuda(idkorisnik=p1)
    o1 = Ponuda(idkorisnik=p1)
    o2 = Ponuda(idkorisnik=p1)
    o3 = Ponuda(idkorisnik=p1)


    wines = []
    wines.append(Vino())

    print("Success")
