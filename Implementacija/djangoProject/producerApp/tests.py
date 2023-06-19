"""
    Author: Aleksa Boricic 2020/0294
    Automatically generated by Django
"""
from django.contrib.auth.models import Group
from django.test import TestCase
from baza.models import *
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
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
        cls.group1.save()
        cls.group1.user_set.add(cls.p1)

    def test_for_producder_redirect(self):
        response = self.client.post('/user/add/myStore')
        self.assertEquals(response.status_code, 302)

    def test_add_wine_no_tags(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        response = self.client.post(reverse('viewWine'), {
            'wineName': 'Vino123',
            'price': '800',
            'description': 'veoma lepo vino',
            'winePicture': SimpleUploadedFile('/images/barbara.jpg', open('/images/barbara.jpg', 'rb')).read(),
            'taginputs': 'roze'
        })
        offer = Ponuda.objects.all()
        new_wine = None
        for off in offer:
            wine = Vino.objects.get(idponuda=off)
            if wine.naziv == 'Vino123':
                new_wine = wine
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(offer)
        self.assertIsNotNone(new_wine)

    def test_add_celebration(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        response = self.client.post(reverse('inpurtCelebration'), {
            'price': '35',
            'capacity': '78',
            'description': 'veoma lepa sala',
            # 'winePicture': SimpleUploadedFile('/static/images/barbara.jpg', open('/static/images/barbara.jpg', 'rb')).read(),
        })
        offer = Ponuda.objects.filter(idkorisnik=self.p1)
        self.assertEquals(response.status_code, 302)
        self.assertIsNotNone(offer)

    def test_check_if_tour_exists(self):
        self.client.login(username='bojana0507@hotmail.com', password='Vinarijakis123')
        
