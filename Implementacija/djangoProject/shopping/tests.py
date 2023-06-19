import datetime

from django.test import TestCase

from baza.models import *


class shoppingApp(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.p1 = Proizvodjac.objects.create_user(password="Vinarijakis123", imefirme="Vinarija Kis",
                                                 registarskibroj=1234,
                                                 brtelefona="+381645565656", adresa="Bulevar Oslobodjenja 67, Novi Sad",
                                                 opis="Mala porodicna vinarija puna ljubavi",
                                                 javnoime="Vinarija Kis", email="bojana0507@hotmail.com",
                                                 logo="images/1234.jpg")
        cls.p1.save()
        cls.k1 = Kupac.objects.create_user(password="Jovana1234", first_name="Jovana", last_name="Mitic",
                                           brtelefona="+3817887877", adresa="Negde daleko",
                                           javnoime="Jovana Mitic",
                                           datumrodjenja=datetime.datetime(year=2002, month=1, day=16),
                                           email="jovanamitic@gmail.com")
        cls.k1.save()
        cls.offer1 = Ponuda(idkorisnik=cls.p1)
        cls.offer1.save()
        cls.wine1 = Vino(idponuda=cls.offer1, naziv="Aalto", cena=1200,
                         opisvina="Aalto Aalto 2020 je suvo crveno vino dobijeno od sorte grožđa Tempranillo 100%",
                         brojprodatih=10)
        cls.wine1.save()
        cls.offer2 = Ponuda(idkorisnik=cls.p1)
        cls.offer2.save()
        cls.wine2 = Vino(idponuda=cls.offer2, naziv="Drugo", cena=3400,
                         opisvina="Opis vina",
                         brojprodatih=15)
        cls.pic2 = Slika(idponuda_id=cls.wine2.idponuda_id, slika='neka.jpg')
        cls.pic2.save()
        cls.wine2.save()

        cls.offer3 = Ponuda(idkorisnik=cls.p1)
        cls.offer3.save()

        cls.offerSpace = Ponudaprostor(idponuda=cls.offer3)
        cls.offerSpace.save()
        cls.tour = Obilazak(idponuda=cls.offerSpace, cenasomelijera=1200)
        cls.tour.save()
        cls.sommelier = Somelijer(idponuda=cls.tour, ime='Jovan', biografija='Biografija', slika='somelijer.jpg')
        cls.sommelier.save()

        cls.typeOfTour = Vrstaobilaska(idponuda=cls.tour, opis='Lepo', cena=2000, naziv='Obilazak1')
        cls.typeOfTour.save()

        cls.offer4 = Ponuda(idkorisnik=cls.p1)
        cls.offer4.save()

        cls.offerSpace1 = Ponudaprostor(idponuda=cls.offer4)
        cls.offerSpace1.save()
        cls.celebration = Proslava(idponuda=cls.offerSpace1, kapacitet=50, cenapoosobi=50, opisproslave='Neki opis')
        cls.celebration.save()

        cls.tag1 = Tag(idponuda=cls.wine1, tag="Prvi tag")
        cls.tag1.save()

        cls.tag2 = Tag(idponuda=cls.wine2, tag="Drugi tag")
        cls.tag2.save()

        cls.questionnaire = Upitnikpitanje(tekst="Prvo pitanje")
        cls.questionnaire.save()

        cls.answer1 = Upitnikodgovor(idpitanje=cls.questionnaire, odgovor="Prvi odgovor", idtag=cls.tag1)
        cls.answer1.save()

        cls.answer2 = Upitnikodgovor(idpitanje=cls.questionnaire, odgovor="Drugi odgovor", idtag=cls.tag2)
        cls.answer2.save()

    def test_shoppingCart_redirect(self):
        response = self.client.post('/shopping/shoppingCart')
        self.assertEquals(response.status_code, 302)

    def test_shoppingDone_redirect(self):
        response = self.client.post('/shopping/shoppingDone')
        self.assertEquals(response.status_code, 302)

    def test_reservationCelebrationDone_redirect(self):
        response = self.client.post('/shopping/reservationCelebrationDone')
        self.assertEquals(response.status_code, 302)

    def test_addToCartNewItem(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')
        response = self.client.post('/shopping/addToCart',
                                    {'idItem': self.wine1.idponuda_id,
                                     'quantity': 2}
                                    )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ukorpi.objects.filter().exists())

        # Verify that the cart contains the correct product
        cart = Ukorpi.objects.get(idkorisnik_id=self.k1.id)
        self.assertEqual(cart.kolicina, 2)
        self.assertEqual(cart.idponuda_id, self.wine1.idponuda_id)

    def test_addToCartExistingItem(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')
        inCart = Ukorpi(idkorisnik=self.k1, idponuda=self.wine1, kolicina=5)
        inCart.save()

        response = self.client.post('/shopping/addToCart',
                                    {'idItem': self.wine1.idponuda_id,
                                     'quantity': 2}
                                    )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ukorpi.objects.filter().exists())

        # Verify that the cart contains the correct product and quantity
        cart = Ukorpi.objects.get(idkorisnik_id=self.k1.id)
        self.assertEqual(cart.kolicina, 7)
        self.assertEqual(cart.idponuda_id, self.wine1.idponuda_id)

    def test_deleteCartItem(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')
        inCart = Ukorpi(idkorisnik=self.k1, idponuda=self.wine2, kolicina=5)
        inCart.save()

        response = self.client.post('/shopping/shoppingCart/deleteItem',
                                    {'itemId': self.wine2.idponuda_id}
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Ukorpi.objects.filter(idponuda_id=self.wine2.idponuda_id, idkorisnik=self.k1).exists())

    def test_changeItemQuantity(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')
        inCart = Ukorpi(idkorisnik=self.k1, idponuda=self.wine2, kolicina=5)
        inCart.save()
        inCart2 = Ukorpi(idkorisnik=self.k1, idponuda=self.wine1, kolicina=2)
        inCart2.save()

        response = self.client.post('/shopping/shoppingCart/changeQuantity',
                                    {'itemId': self.wine2.idponuda_id,
                                     'newQuantity': 16}
                                    )
        self.assertEqual(response.status_code, 200)
        cart = Ukorpi.objects.get(idkorisnik_id=self.k1.id, idponuda_id=self.wine2.idponuda_id)
        self.assertEqual(cart.kolicina, 16)

        cart = Ukorpi.objects.get(idkorisnik_id=self.k1.id, idponuda_id=self.wine1.idponuda_id)
        self.assertEqual(cart.kolicina, 2)

    def test_emptyCart(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')
        inCart = Ukorpi(idkorisnik=self.k1, idponuda=self.wine2, kolicina=5)
        inCart.save()

        response = self.client.post('/shopping/shoppingCart/emptyCart')
        self.assertEqual(response.status_code, 302)
        cart = Ukorpi.objects.filter(idkorisnik_id=self.k1.id)
        self.assertEqual(cart.count(), 0)

    def test_shoppingCartShow(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')
        inCart = Ukorpi(idkorisnik=self.k1, idponuda=self.wine2, kolicina=5)
        inCart.save()

        response = self.client.get('/shopping/shoppingCart')
        self.assertContains(response, 'Drugo')
        self.assertNotContains(response, 'Neko drugo ime')
        self.assertTemplateUsed(response, 'korpaZaKupovinu.html')

    def test_shoppingDoneEmpryCart(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')
        response = self.client.get('/shopping/shoppingDone')
        self.assertEqual(response.status_code, 302)

    def test_shoppingDone(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')
        inCart = Ukorpi(idkorisnik=self.k1, idponuda=self.wine2, kolicina=5)
        inCart.save()
        prevQ = self.wine2.brojprodatih
        self.client.post('/shopping/shoppingDone',
                         {'sumPrices[]': self.wine2.cena})

        self.assertEqual(prevQ + 5, Vino.objects.get(idponuda_id=self.wine2.idponuda_id).brojprodatih)
        cart = Ukorpi.objects.filter(idkorisnik_id=self.k1.id)
        self.assertEqual(cart.count(), 0)

    def test_tourReservation(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')

        response = self.client.post('/shopping/reservationVisitDone',
                                    {'date': datetime.date.today(),
                                     'quantity': 2,
                                     'somelijer': 'Jovan',
                                     'obilazak': self.typeOfTour.pk})

        appointments = Termin.objects.filter(idponuda_id=self.tour.idponuda_id, vreme=datetime.date.today(),
                                             brojljudi=2)
        self.assertEqual(appointments.count(), 1)

        reservations = Rezervacija.objects.filter(idkorisnik=self.k1, idtermin=appointments.first())
        self.assertEqual(reservations.count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_reservationCelebration(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')

        response = self.client.post('/shopping/reservationCelebrationDone',
                                    {'date': datetime.date.today(),
                                     'quantity': 200,
                                     'price': self.celebration.cenapoosobi,
                                     'celebrationId': self.celebration.pk})

        appointments = Termin.objects.filter(idponuda_id=self.celebration.idponuda_id, vreme=datetime.date.today(),
                                             brojljudi=200)
        self.assertEqual(appointments.count(), 1)

        reservations = Rezervacija.objects.filter(idkorisnik=self.k1, idtermin=appointments.first())
        self.assertEqual(reservations.count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_questionnaire(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')
        response = self.client.post('/shopping/questionnaireQ')
        self.assertContains(response, 'Prvo pitanje')
        self.assertContains(response, 'Prvi odgovor')
        self.assertContains(response, 'Drugi odgovor')
        self.assertNotContains(response, 'Neko drugo ime')

    def test_questionnaireResult(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')
        self.client.post('/shopping/questionnaireRes',
                         {'question1': 'Drugi tag'})

        results = Rezultatupitnika.objects.filter(idkorisnik=self.k1)
        self.assertEqual(results.count(), 1)
        self.assertEqual(Rezultatupitnika.objects.all().first().idtag.tag, 'Drugi tag')

    def test_questionnaireHist(self):
        self.client.login(username='jovanamitic@gmail.com', password='Jovana1234')
        result = Rezultatupitnika(idkorisnik=self.k1, idtag=self.tag2)
        result.save()

        response = self.client.get('/shopping/questionnaireHist')
        self.assertContains(response, 'Drugi tag')
        self.assertNotContains(response, 'Neko drugo ime')
