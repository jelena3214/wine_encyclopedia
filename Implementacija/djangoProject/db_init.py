import datetime
import random
from datetime import date, timedelta

from django.contrib.auth.models import Group

from baza.models import *


def random_datetime_future():
    current_datetime = datetime.datetime.now()
    days_to_add = random.randint(1, 365)
    hours_to_add = random.randint(0, 23)
    minutes_to_add = random.randint(0, 59)

    future_datetime = current_datetime + datetime.timedelta(days=days_to_add, hours=hours_to_add,
                                                            minutes=minutes_to_add)
    return future_datetime


def init():
    groups = []
    groups.append(Group(name="Kupci"))
    groups.append(Group(name="Proizvodjaci"))
    [x.save() for x in groups]

    admin = Korisnik.objects.create_superuser(email="admin@admin.com", password="Admin123")
    admin.save()

    producers = []
    producerGroup = Group.objects.get(name='Proizvodjaci')
    p1 = Proizvodjac.objects.create_user(password="Vinarijakis123", imefirme="Vinarija Kis", registarskibroj=1234,
                                         brtelefona="+381645565656", adresa="Bulevar Oslobodjenja 67, Novi Sad",
                                         opis="Mala porodicna vinarija puna ljubavi",
                                         javnoime="Vinarija Kis", email="bojana0507@hotmail.com", logo="images/1234.jpg")

    producerGroup.user_set.add(p1)
    p2 = Proizvodjac.objects.create_user(password="Vinarijabogdan123", imefirme="Vinarija Zvonko Bogdan",
                                         registarskibroj=1237,
                                         brtelefona="+381645565690", adresa="Palicko jezero",
                                         opis="Dodjite da pijemo zajedno i veselimo se!",
                                         javnoime="Zvonko Bogdan", email="zvonkoBogdan111@gmail.com", logo="images/1237.png")
    producerGroup.user_set.add(p2)

    p3 = Proizvodjac.objects.create_user(password="Novasansa123", imefirme="Vinarija Nova Sansa", registarskibroj=1277,
                                         brtelefona="+381645589690", adresa="Kragujevac",
                                         opis="Porodicna vinarija",
                                         javnoime="Nova Sansa", email="novaSansa111@gmail.com", logo='images/1277.png')
    producerGroup.user_set.add(p3)
    producers.append(p1)
    producers.append(p2)
    producers.append(p3)
    [x.save() for x in producers]

    buyers = []
    buyersGroup = Group.objects.get(name='Kupci')
    b1 = Kupac.objects.create_user(password="Jovana1234", first_name="Jovana", last_name="Mitic",
                                   brtelefona="+3817887877", adresa="Negde daleko",
                                   javnoime="Jovana Mitic", datumrodjenja=datetime.datetime(year=2002, month=1, day=16),
                                   email="jovanamitic@gmail.com")

    buyersGroup.user_set.add(b1)
    b2 = Kupac.objects.create_user(password="Bojana1234", first_name="Bojana", last_name="Malesevic",
                                   brtelefona="+3878887877", adresa="Despotovac",
                                   javnoime="Bojana Malesevic",
                                   datumrodjenja=datetime.datetime(year=2001, month=7, day=5),
                                   email="malesevic.bojana0507@gmail.com")
    buyersGroup.user_set.add(b2)

    b3 = Kupac.objects.create_user(password="Aleksa1234", first_name="Aleksa", last_name="Boricic",
                                   brtelefona="+3817866577", adresa="Novi Beograd",
                                   javnoime="Aleksa Boricic",
                                   datumrodjenja=datetime.datetime(year=2001, month=1, day=26),
                                   email="aleksaboricic@gmail.com")
    buyersGroup.user_set.add(b3)

    b4 = Kupac.objects.create_user(password="Jelena1234", first_name="Jelena", last_name="Cvetic",
                                   brtelefona="+3817943577", adresa="Guncati",
                                   javnoime="Jelena Cvetic",
                                   datumrodjenja=datetime.datetime(year=2001, month=3, day=26),
                                   email="jelenacvetic@gmail.com")
    buyersGroup.user_set.add(b4)
    buyers.append(b1)
    buyers.append(b2)
    buyers.append(b3)
    buyers.append(b4)
    [x.save() for x in buyers]

    offers = []
    offersPhoto = []
    for i in range(9):
        if i % 3 == 0:
            tmpOff = Ponuda(idkorisnik=p1)
        elif i % 3 == 1:
            tmpOff = Ponuda(idkorisnik=p2)
        else:
            tmpOff = Ponuda(idkorisnik=p3)
        tmpOff.save()
        offersPhoto.append(Slika(idponuda=tmpOff, slika='images/' + tmpOff.idkorisnik.javnoime + str(tmpOff.idponuda) + ".jpg"))
        offers.append(tmpOff)

    [x.save() for x in offersPhoto]

    wines = [Vino(idponuda=offers[0], naziv="Aalto", cena=1200,
                  opisvina="Aalto Aalto 2020 je suvo crveno vino dobijeno od sorte grožđa Tempranillo 100%",
                  brojprodatih=10),
             Vino(idponuda=offers[1], naziv="Nebo Tamjanika", cena=1430,
                  opisvina="Deveto nebo Tamjanika 2022 je belo vino dobijeno od istoimene sorte grožđa",
                  brojprodatih=46),
             Vino(idponuda=offers[2], naziv="Adega de Pegoes Rose", cena=695,
                  opisvina="Adega de Pegoes Rose je vino napravljeno od sorti Castelao i Aragonez",
                  brojprodatih=80)]

    tags = []
    tagDesc = ['Belo', 'Crveno', 'Roze']
    for i in range(3):
        tags.append(Tag(idponuda=wines[i], tag=tagDesc[i]))

    [x.save() for x in wines]
    [x.save() for x in tags]

    tourOffers = []

    for i in range(3, 9):
        tmp = Ponudaprostor(idponuda=offers[i])
        tourOffers.append(tmp)

    [x.save() for x in tourOffers]

    tours = []
    sommeliers = []
    names = ['Marko', 'Jovan', 'Anja', 'Sonja', 'Aleksa', 'Stjepan']
    for i in range(3):
        newTour = Obilazak(idponuda=tourOffers[i], cenasomelijera=random.randint(800, 1400))
        newTour.save()
        tours.append(newTour)
        for j in range(2):
            tmpSom = Somelijer(idponuda=newTour, ime=names[i * 2 + j], biografija="Moja biografija " + names[i * 2 + j],
                               slika='images/' + names[i * 2 + j])
            tmpSom.save()
            tmpSom.slika = str(tmpSom.slika) + str(tmpSom.pk) + ".jpg"
            tmpSom.save()
            sommeliers.append(tmpSom)

    descriptions = [
        'Doživite čari nastanka vina i u prelepom ambijentu uživajte u degustaciji vina koja nose pečat Palićkog vinogorja.',
        'Naši obilasci obuhvataju staze i predele, kulturu i običaje, vino i gastronomiju. Iskustvo generacija vinara na ovom područiju približiće vam filozofiju i umetnost u stvaranju karaktera vina.',
        'Obilaskom naše vinarije približićemo Vam razvojni put naše vinarije, Fruškogorske vinske regije i dočaraćemo vam magiju proizvodnje naših vina. Dođite da uživamo zajedno i ponesite sa sobom lepe uspomene.']
    typeOfTour = []
    for i in range(3):
        typeOfTour.append(Vrstaobilaska(idponuda=tours[i], opis=descriptions[i],
                                        naziv=tours[i].idponuda.idponuda.idkorisnik.javnoime + " obilazak",
                                        cena=random.randint(1500, 2000)))
    [x.save() for x in typeOfTour]

    spaces = []
    descriptions = [
        'Poštovani, Izdajemo dvorište sa bazenom i vinskom salom za sve vrste proslava i događaja. Takođe u cenu je uključen i obilazak vinarije, kao i degustacija vina i edukacija o istoriji vinarstva.',
        'Najlepše životne trenutke valja proslaviti na mestu dostojnom istih, a naš tim će se potruditi da bude najbolji domaćin. Bilo da je u pitanju rođendan, godišnjica, ili neki drugi poseban trenutak vredan slavlja, naš ambijent u kominaciji sa posvećenošću našeg osoblja, nikoga neće ostaviti ravnodušnim.',
        'Za potrebe proslava može se koristiti čitav kompleks vinarije, bazeni i prostor oko bazena čak i grabov šumarak. ']
    j = 0
    for i in range(3, 6):
        spaces.append(
            Proslava(idponuda=tourOffers[i], cenapoosobi=random.randint(2000, 4000), kapacitet=random.randint(50, 200),
                     opisproslave=descriptions[j]))
        j += 1

    [x.save() for x in spaces]

    tourOffers = []
    tourTime = []

    for i in range(len(tours)):
        for j in range(random.randint(1, 3)):
            tourTime.append(Termin(idponuda=tours[i].idponuda,
                                   vreme=date.today() + datetime.timedelta(days=random.randint(1, 365)),
                                   brojljudi=random.randint(1, 20)))

    for i in range(len(spaces)):
        for j in range(random.randint(1,3)):
            tourTime.append(Termin(idponuda=spaces[i].idponuda,
                            vreme=date.today() + datetime.timedelta(days=random.randint(1, 365)),
                            brojljudi=random.randint(1, spaces[i].kapacitet)))

    [x.save() for x in tourOffers]
    [x.save() for x in tourTime]

    reservations = []

    for i in range(len(tourTime)):
        reservations.append(Rezervacija(idtermin=tourTime[i], idkorisnik=buyers[random.randint(0, len(buyers)-1)]))

    [r.save() for r in reservations]


    subscriptionType = [Pretplata(naslov="GODIŠNJI PAKET", cena=1000,
                                  opis='Proizvodi vinarije su istaknuti na početnoj stranici.Naplata na svakih godinu dana do otkazivanja.'),
                        Pretplata(naslov='PREMIUM  GODIŠNJI PAKET', cena=1600,
                                  opis='Obilazak vinarije je istaknut na početnoj stranici. Naplata na svakih godinu dana do otkazivanja.'),
                        Pretplata(naslov='JEDNOKRATNI PAKET', cena=2000,
                                  opis='Proizvodi vinarije su istaknuti na početnoj stranici u trajanju od mesec dana.'),
                        Pretplata(naslov='PREMIUM  JEDNOKRATNI PAKET', cena=3000,
                                  opis='Obilazak vinarije je istaknut na početnoj straniciu trajanju od mesec dana.')]
    [x.save() for x in subscriptionType]

    reviews = [Recenzija(idponuda=wines[0].idponuda, idkorisnik=buyers[0], opisrec='Mnogo dobro vino', ocena=5),
               Recenzija(idponuda=wines[1].idponuda, idkorisnik=buyers[2], opisrec="Okej je", ocena=3),
               Recenzija(idponuda=wines[1].idponuda, idkorisnik=buyers[1], opisrec="Dobro", ocena=4)]

    [x.save() for x in reviews]

    producersSubscriptions = [
        Pretplacen(idpretplata=subscriptionType[0], idkorisnik=producers[0], trenutnistatus='',
                   datumpocetak=date.today(),
                   datumkraj=date(year=date.today().year + 1, day=date.today().day, month=date.today().month)),

        Pretplacen(idpretplata=subscriptionType[1], idkorisnik=producers[2], trenutnistatus='',
                   datumpocetak=date.today(),
                   datumkraj=date(year=date.today().year + 1, day=date.today().day, month=date.today().month))
    ]

    [x.save() for x in producersSubscriptions]

    questions = [
        Upitnikpitanje(tekst="Izaberite piće:"),
        Upitnikpitanje(tekst="Koja Vam je omiljena vrsta čokolade?")
    ]

    answers = [
        Upitnikodgovor(idpitanje=questions[0], odgovor="Hladna kokosova voda", idtag=Tag.objects.get(tag="Belo")),
        Upitnikodgovor(idpitanje=questions[0], odgovor="Sveže ceđeni sok", idtag=Tag.objects.get(tag="Crveno")),
        Upitnikodgovor(idpitanje=questions[0], odgovor="Voćni šejk", idtag=Tag.objects.get(tag="Roze")),
        Upitnikodgovor(idpitanje=questions[1], odgovor="Mlečna čokolada", idtag=Tag.objects.get(tag="Crveno")),
        Upitnikodgovor(idpitanje=questions[1], odgovor="Crna čokolada", idtag=Tag.objects.get(tag="Belo")),
        Upitnikodgovor(idpitanje=questions[1], odgovor="Bela čokolada", idtag=Tag.objects.get(tag="Roze"))
    ]

    [x.save() for x in questions]
    [x.save() for x in answers]

    print("Success")
