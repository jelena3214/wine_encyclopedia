"""
    Author: Jovana Mitic 2020/0315
    Automatically generated by Django
"""
from django.contrib.auth.models import Group
from django.test import TestCase
from baza.models import *
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from datetime import date, datetime
import random


# Create your tests here.


class ProducerAppTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.p1 = Proizvodjac.objects.create_user(password="Vinarijakis123", imefirme="Vinarija Kis",
                                                 registarskibroj=1234,
                                                 brtelefona="+381645565656", adresa="Bulevar Oslobodjenja 67, Novi Sad",
                                                 opis="Mala porodicna vinarija puna ljubavi",
                                                 javnoime="Vinarija Kis", email="bojana0507@hotmail.com",
                                                 logo="images/1234.jpg")
        cls.p1.save()
        cls.group1 = Group(name='Proizvodjaci')
        cls.group2 = Group(name='Kupci')
        cls.group1.save()
        cls.group2.save()
        cls.group1.user_set.add(cls.p1)
        cls.pretplata1 = Pretplata(naslov="GODIŠNJI PAKET", cena=1000,
                                   opis='Proizvodi vinarije su istaknuti na početnoj stranici.Naplata na svakih godinu dana do otkazivanja.')
        cls.pretplata2 = Pretplata(naslov='JEDNOKRATNI PAKET', cena=2000,
                                   opis='Proizvodi vinarije su istaknuti na početnoj stranici u trajanju od mesec dana.')
        cls.pretplata1.save()
        cls.pretplata2.save()

    def test_for_producder_redirect(self):
        response = self.client.post('/user/add/myStore')
        self.assertEquals(response.status_code, 302)

    def test_add_wine_no_tags(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        response = self.client.post(reverse('viewWine'), {
            'wineName': 'Vino123',
            'price': '800',
            'description': 'veoma lepo vino',
            'winePicture': SimpleUploadedFile('images/barbara.jpg', open('static/images/barbara.jpg', 'rb').read()),
            'taginputs': ''
        })
        offer = Ponuda.objects.all()
        new_wine = None
        for off in offer:
            wine = Vino.objects.get(idponuda=off)
            if wine.naziv == 'Vino123':
                new_wine = wine
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(new_wine)
        self.assertEqual(new_wine.naziv, "Vino123")
        self.assertEqual(new_wine.cena, 800)
        self.assertEqual(new_wine.opisvina, "veoma lepo vino")
        slika = Slika.objects.get(idponuda_id=new_wine.idponuda).slika
        self.assertRegex(slika.name, r"^images/barbara_[a-zA-Z0-9]{7}\.jpg$")

        if os.path.exists(slika.path):
            os.remove(slika.path)

    def test_add_celebration(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        response = self.client.post(reverse('inpurtCelebration'), {
            'price': '35',
            'capacity': '78',
            'description': 'veoma lepa sala',
            'inputTourPicture': SimpleUploadedFile('images/barbara.jpg',
                                                   open('static/images/barbara.jpg', 'rb').read()),
        })
        offer = Ponuda.objects.filter(idkorisnik=self.p1)
        new_celebration = None
        for off in offer:
            off_space = Ponudaprostor.objects.get(idponuda=off)
            celebration = Proslava.objects.get(idponuda=off_space)
            if celebration.opisproslave == 'veoma lepa sala':
                new_celebration = celebration
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(new_celebration)
        self.assertEqual(new_celebration.cenapoosobi, 35)
        self.assertEqual(new_celebration.kapacitet, 78)
        self.assertEqual(new_celebration.opisproslave, 'veoma lepa sala')
        slika = Slika.objects.get(idponuda=new_celebration.idponuda.idponuda).slika
        self.assertRegex(slika.name, r"^images/barbara_[a-zA-Z0-9]{7}\.jpg$")

        if os.path.exists(slika.path):
            os.remove(slika.path)

    def test_no_tours(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        response = self.client.post('/user/add/addTourType', {
            'tourDescription': 'veoma lep obilazak',
            'tourName': 'premium',
            'tourPrice': '2000'
        })
        offer = Ponuda.objects.filter(idkorisnik=self.p1)
        self.assertEquals(len(offer), 1)
        self.assertEquals(response.status_code, 200)

    def test_tours_exist(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        offer = Ponuda(idkorisnik=self.p1)
        offer.save()
        offer_space = Ponudaprostor(idponuda=offer)
        offer_space.save()
        tour = Obilazak(idponuda=offer_space)
        tour.save()
        basic_tour = Vrstaobilaska(idponuda=tour, naziv="Basic", cena=1500, opis="Veoma lep obilazak")
        basic_tour.save()
        response = self.client.post('/user/add/addTourType', {
            'tourDescription': 'veoma lep obilazak',
            'tourName': 'premium',
            'tourPrice': '2000'
        })
        tour = Obilazak.objects.get(idponuda__idponuda__idkorisnik=self.p1)
        tour_types = Vrstaobilaska.objects.filter(idponuda=tour)
        self.assertEquals(len(tour_types), 2)
        self.assertEquals(response.status_code, 200)

    def test_add_sommelier(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        file_content = b"File content goes here"
        file = SimpleUploadedFile("myfile.txt", file_content)
        response = self.client.post('/user/add/addSommelier',
                                    {'sommelierName': 'Ime',
                                     'sommelierDescription': 'Opis',
                                     'sommelierPicture': file}
                                    )
        sommelierNum = Somelijer.objects.all().count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(sommelierNum, 1)

    def test_remove_sommelier(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        offer = Ponuda(idkorisnik=self.p1)
        offer.save()
        offerTour = Ponudaprostor(idponuda=offer)
        offerTour.save()
        tour = Obilazak(idponuda=offerTour, cenasomelijera=1200)
        tour.save()
        newSommelier = Somelijer(ime='Jovana', biografija='Moja biografija', slika='slika.jpg', idponuda=tour)
        newSommelier.save()
        response = self.client.get('/user/add/removeSommelier/' + str(newSommelier.pk) + '/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Somelijer.objects.all().count(), 0)

    def test_subscribe_first(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        response = self.client.post('/user/add/subscribeAd/' + str(self.pretplata1.idpretplata))

        pretplaceni = Pretplacen.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(pretplaceni), 1)

    def test_subscribed_more(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        new_subsc = Pretplacen(idpretplata=self.pretplata1, idkorisnik=self.p1, datumpocetak=date(2023, 1, 16),
                               datumkraj=date.today(), trenutnistatus='aktivna')
        new_subsc.save()
        response = self.client.post('/user/add/subscribeAd/' + str(self.pretplata1.idpretplata))
        self.assertEqual(response.status_code, 200)

    def test_unsubscribe(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        new_subsc = Pretplacen(idpretplata=self.pretplata1, idkorisnik=self.p1, datumpocetak=date(2023, 1, 16),
                               datumkraj=date.today(), trenutnistatus='aktivna')
        new_subsc.save()
        response = self.client.post('/user/add/unsubscribeAd/' + str(self.pretplata1.idpretplata))
        self.assertEqual(response.status_code, 302)

    def test_delete_reservation(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        kupac = Kupac.objects.create_user(password="Aleksa1234", first_name="Aleksa", last_name="Boricic",
                                          brtelefona="+3817866577", adresa="Novi Beograd",
                                          javnoime="Aleksa Boricic",
                                          datumrodjenja=datetime(year=2001, month=1, day=26),
                                          email="aleksaboricic@gmail.com")
        kupac.save()
        self.group2.user_set.add(kupac)
        ponuda = Ponuda(idkorisnik=self.p1)
        ponuda.save()
        ponudaprostor = Ponudaprostor(idponuda=ponuda)
        ponudaprostor.save()
        obilazak = Obilazak(idponuda=ponudaprostor, cenasomelijera=random.randint(800, 1400))
        obilazak.save()
        vrstaobilaska = Vrstaobilaska(idponuda=obilazak, opis="Mnogo lep obilazak, degustacija 4 vina",
                                      naziv=obilazak.idponuda.idponuda.idkorisnik.javnoime + " obilazak",
                                      cena=random.randint(1500, 2000))
        vrstaobilaska.save()
        termin = Termin(idponuda=ponudaprostor, brojljudi=15, vreme=date(2023, 6, 20))
        termin.save()
        rezervacija = Rezervacija(idkorisnik=Korisnik.objects.get(id=kupac.id), idtermin=termin)
        rezervacija.save()
        response = self.client.post('/user/add/removeReservation/' + str(termin.idtermin))
        termini = Termin.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(termini), 0)
