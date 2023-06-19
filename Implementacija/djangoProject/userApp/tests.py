from datetime import datetime
import os
from django.contrib.auth.models import Group
from django.urls import reverse
from baza.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
"""
    Author: Bojana Malesevic 2020/0235
"""


class UserRegistrationTestCase(TestCase):

    existingBuyer = None
    existingProducer = None

    @classmethod
    def setUpClass(cls):
        cls.group = Group(name='Kupci')
        cls.group.save()
        cls.group = Group(name='Proizvodjaci')
        cls.group.save()
        cls.existingBuyer = Kupac.objects.create_user(
            email='existinguser@example.com',
            password='testpassword',
            first_name='Jane',
            last_name='Smith',
            brtelefona='987654321',
            adresa='Ulica 1',
            datumrodjenja=datetime(year=1995, month=7, day=17),
        )
        cls.existingBuyer.groups.add(Group.objects.get(name='Kupci'))
        cls.existingBuyer.save()

        cls.existingProducer = Proizvodjac.objects.create_user(
            email='existingproducer@example.com',
            password='testpassword',
            imefirme='Existing Winery',
            registarskibroj='54321',
            brtelefona='987654321',
            adresa='456 Vineyard St',
            opis='Existing winery description',
            logo=SimpleUploadedFile('images/1234.jpg', open('static/images/1234.jpg', 'rb').read())
        )
        cls.existingProducer.groups.add(Group.objects.get(name='Proizvodjaci'))
        cls.existingProducer.save()

    @classmethod
    def tearDownClass(cls):
        # Clean up code after all tests
        if os.path.exists(cls.existingProducer.logo.path):
            os.remove(cls.existingProducer.logo.path)

    def test_register_user(self):
        response = self.client.post(reverse('registerUser'), {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'firstName': 'John',
            'lastName': 'Doe',
            'phoneNumber': '123456789',
            'address': 'Street 123',
            'birthDate': '1990-01-01',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loginUser'))

        # Check if the user is created in the database
        user = Korisnik.objects.get(email='testuser@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.kupac.brtelefona, '123456789')
        self.assertEqual(user.kupac.adresa, 'Street 123')

        # Check if the user is assigned to the 'Kupci' group
        kupciGroup = Group.objects.get(name='Kupci')
        self.assertIn(kupciGroup, user.groups.all())

    def test_register_existing_user(self):
        response = self.client.post(reverse('registerUser'), {
            'email': 'existinguser@example.com',
            'password': 'testpassword',
            'firstName': 'Jane',
            'lastName': 'Smith',
            'phoneNumber': '987654321',
            'address': '456 Elm St',
            'birthDate': '1995-01-01',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registracijaKupac.html')
        self.assertContains(response, 'Već postoji nalog sa unetom email adresom')

    def test_register_producer(self):
        response = self.client.post(reverse('registerProducer'), {
            'email': 'testproducer@example.com',
            'password': 'testpassword',
            'name': 'Test Winery',
            'companyNumber': '12345',
            'phoneNumber': '123456789',
            'address': '123 Vineyard St',
            'description': 'Test winery description',
            'logo': SimpleUploadedFile('images/1234.jpg', open('static/images/1234.jpg', 'rb').read())
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loginUser'))

        # Check if the producer is created in the database
        producer = Proizvodjac.objects.get(email='testproducer@example.com')
        self.assertEqual(producer.imefirme, 'Test Winery')
        self.assertEqual(producer.javnoime, 'Test Winery')
        self.assertEqual(producer.registarskibroj, 12345)
        self.assertEqual(producer.brtelefona, '123456789')
        self.assertEqual(producer.adresa, '123 Vineyard St')
        self.assertEqual(producer.opis, 'Test winery description')
        self.assertRegex(producer.logo.name, r"^images/1234_[a-zA-Z0-9]{7}\.jpg$")

        # Check if the producer is assigned to the 'Proizvodjaci' group
        proizvodjaciGroup = Group.objects.get(name='Proizvodjaci')
        self.assertIn(proizvodjaciGroup, producer.groups.all())

        if os.path.exists(producer.logo.path):
            os.remove(producer.logo.path)

    def test_register_existing_producer(self):
        response = self.client.post(reverse('registerProducer'), {
            'email': 'existingproducer@example.com',
            'password': 'testpassword',
            'name': 'Existing Winery',
            'companyNumber': '54321',
            'phoneNumber': '987654321',
            'address': '456 Vineyard St',
            'description': 'Existing winery description',
            'logo': SimpleUploadedFile('images/1234.jpg', open('static/images/1234.jpg', 'rb').read())
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registracijaProizvodjac.html')
        self.assertContains(response, 'Već postoji nalog sa unetom email adresom')

    def test_login_user(self):
        response = self.client.post(reverse('loginUser'), {
            'email': 'existinguser@example.com',
            'password': 'testpassword',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Check if the user is authenticated
        user = Korisnik.objects.get(email='existinguser@example.com')
        self.assertTrue(user.is_authenticated)

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('loginUser'), {
            'email': 'existinguser@example.com',
            'password': 'wrongpassword',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Pogresna lozinka ili email adresa')
