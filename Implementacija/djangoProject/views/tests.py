from django.test import TestCase
from baza.models import *

"""
    Author: Aleksa Boricic 2020/0294
"""


# Helper Functions
def createUser(username, password):
    user = Proizvodjac()
    user.javnoime = "Naidobrata Firma"
    user.registarskibroj = 7777
    user.opis = "Nasata firma nasata momiceta se nomere 1"
    user.username = username
    user.set_password(password)
    user.save()
    return user


def createOffer(user):
    offer = Ponuda()
    offer.idkorisnik = user
    offer.save()
    return offer


def createOfferSpace(offer):
    offerspace = Ponudaprostor(idponuda=offer)
    offerspace.save()
    return offerspace


def createWine(naziv, cena, opisVina, offer: Ponuda):
    wine = Vino(naziv=naziv, cena=cena, idponuda=offer)
    wine.save()
    return wine


def createPicture(offer):
    slika = Slika(idponuda=offer)
    slika.save()
    return slika


def createTag(text, wine):
    tag = Tag(tag=text, idponuda=wine)
    tag.save()
    return tag


def createDetour(offerspace, sommelier_price):
    detour = Obilazak(idponuda=offerspace, cenasomelijera=sommelier_price)
    detour.save()
    return detour


def createDetourType(name, price, description, detour):
    detourType = Vrstaobilaska(naziv=name, cena=price, opis=description, idponuda=detour)
    detourType.save()
    return detourType


def createCelebration(offerspace, description, price, capacity):
    celebration = Proslava(idponuda=offerspace, opisproslave=description, cenapoosobi=price, kapacitet=capacity)
    celebration.save()
    return celebration


class ViewTest(TestCase):

    def test_allwines(self):
        user = createUser("TestKorisnik", "T3STS1FR@MIRLJUBAVSRECADECACVECA")
        offer = createOffer(user)
        wine = createWine("Test Vino", 777, "Pravimo cistaka za zdrave plucne maramice", offer)
        slika = createPicture(offer)
        tag = createTag("Belo", wine)
        response = self.client.get("/views/allwines")
        self.assertContains(response, "Test Vino", html=True)

        # Tests if the wine appears at all
        response = self.client.post("/views/allwines", {'winery': user.javnoime})
        self.assertContains(response, "Test Vino", html=True)

        # Tests if the wine appears with all the possible filters and sorts enabled
        response = self.client.post("/views/allwines", {'winery': user.javnoime,
                                                        'sort': 'Po ceni opadajuce',
                                                        'filter': tag.tag})
        self.assertContains(response, "Test Vino", html=True)

    def test_wine_specific(self):
        user = createUser("TestKorisnik", "T3STS1FR@MIRLJUBAVSRECADECACVECA")
        offer = createOffer(user)
        wine = createWine("Test Vino", 777, "TestOpisVina", offer)
        slika = createPicture(offer)
        id = "0" + str(offer.idponuda)

        response = self.client.get("/views/wine/" + id)
        self.assertContains(response, "Test vino", html=True)

    def test_detours(self):
        user = createUser("TestKorisnik", "T3STS1FR@MIRLJUBAVSRECADECACVECA")
        offer = createOffer(user)
        offerspace = createOfferSpace(offer)
        detour = createDetour(offerspace, 1800)
        slika = createPicture(offer)
        detourType = createDetourType("Profi Obilazak", 1700, "Obilazak je veoma profi", detour)

        # Tests if the detour appears when all are displayed
        response = self.client.get("/views/detour")
        self.assertContains(response, user.javnoime, html=True)

        # Tests if the detour appears/doesn't when a filter is applied
        response = self.client.post("/views/detour", {'filter': 'Ima somelijera'})
        self.assertNotContains(response, user.javnoime, html=True)
        response = self.client.post("/views/detour", {'filter': 'Nema somelijera'})
        self.assertContains(response, user.javnoime, html=True)

    def test_detour_specific(self):
        user = createUser("TestKorisnik", "T3STS1FR@MIRLJUBAVSRECADECACVECA")
        offer = createOffer(user)
        offerspace = createOfferSpace(offer)
        detour = createDetour(offerspace, 1800)
        slika = createPicture(offer)
        detourtype = createDetourType("Profi Obilazak", 1700,
                                      "Obilazak je veoma profi", detour)
        detour_id = "0" + user.javnoime
        response = self.client.get("/views/detours/" + detour_id)
        self.assertContains(response, user.javnoime, html=True)
        self.assertContains(response, detourtype.naziv, html=True)

    def test_celebrations(self):
        user = createUser("TestKorisnik", "T3STS1FR@MIRLJUBAVSRECADECACVECA")
        offer = createOffer(user)
        offerspace = createOfferSpace(offer)
        proslava = createCelebration(offerspace, "opis mnogo super proslave", 1700, 100)
        slika = createPicture(offer)
        response = self.client.get("/views/celebration")
        self.assertContains(response, user.javnoime, html=True)

    def test_celebration_specific(self):
        user = createUser("TestKorisnik", "T3STS1FR@MIRLJUBAVSRECADECACVECA")
        offer = createOffer(user)
        offerspace = createOfferSpace(offer)
        proslava = createCelebration(offerspace, "opis mnogo super proslave", 1700, 100)
        slika = createPicture(offer)
        celebration_id = "0" + user.javnoime
        response = self.client.get("/views/celebration/" + celebration_id)
        # Tests if everything appears correctly
        self.assertContains(response, "opis mnogo super proslave", html=True)
        self.assertContains(response, "Kapacitet sale: 100 osoba", html=True)
        self.assertContains(response, "Cena po osobi: 1700 RSD", html=True)
