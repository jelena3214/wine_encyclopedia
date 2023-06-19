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
            javnoime='Jane Smith'
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
            logo=SimpleUploadedFile('images/1234.jpg', open('static/images/1234.jpg', 'rb').read()),
            javnoime='Existing Winery'
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
            'email': self.existingBuyer.email,
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
        self.assertFalse('_auth_user_id' in self.client.session)

        response = self.client.post(reverse('loginUser'), {
            'email': self.existingBuyer.email,
            'password': 'testpassword',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Check if the user is authenticated
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('loginUser'), {
            'email': self.existingBuyer.email,
            'password': 'wrongpassword',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Pogresna lozinka ili email adresa')

    def test_logout_user(self):
        self.assertFalse('_auth_user_id' in self.client.session)
        self.client.login(email=self.existingBuyer.email, password='testpassword')

        user = Korisnik.objects.get(email=self.existingBuyer.email)
        self.assertTrue('_auth_user_id' in self.client.session)

        response = self.client.get(reverse('logoutUser'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Check if the user is logged out
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_change_company_info(self):
        self.client.login(email='existingproducer@example.com', password='testpassword')

        response = self.client.post(reverse('changeCompanyStuff'), {
            'opis': 'New winery description',
            'naziv': 'New Winery Name',
            'logo': SimpleUploadedFile('images/1237.png', open('static/images/1237.png', 'rb').read())
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'promenaInformacijaVinarije.html')

        self.existingProducer = Proizvodjac.objects.get(email=self.existingProducer.email)
        # Check if the producer's information is updated in the database
        self.assertEqual(self.existingProducer.opis, 'New winery description')
        self.assertEqual(self.existingProducer.imefirme, 'New Winery Name')
        self.assertEqual(self.existingProducer.javnoime, 'New Winery Name')
        self.assertRegex(self.existingProducer.logo.name, r"^images/1237_[a-zA-Z0-9]{7}\.png$")

        if os.path.exists(self.existingProducer.logo.path):
            os.remove(self.existingProducer.logo.path)

    def test_change_user_info(self):
        self.client.login(email=self.existingBuyer.email, password='testpassword')

        response = self.client.post(reverse('changeInfoUser'), {
            'showName': 'New User Name',
            'address': 'Ulica 2',
            'phoneNumber': '987654321',
            'currentPassword': 'testpassword',
            'newPassword': 'newpassword',
            'newPasswordSubmit': 'newpassword',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'promenaInformacijaKorisnika.html')

        # Check if the user's information is updated in the database
        self.existingBuyer = Kupac.objects.get(email=self.existingBuyer.email)
        user = Kupac.objects.get(email=self.existingBuyer.email)
        self.assertEqual(self.existingBuyer.javnoime, 'New User Name')
        self.assertEqual(self.existingBuyer.adresa, 'Ulica 2')
        self.assertEqual(self.existingBuyer.brtelefona, '987654321')
        self.assertTrue(self.existingBuyer.check_password('newpassword'))

    def test_change_user_info_change_partially(self):
        self.client.login(email=self.existingBuyer.email, password='testpassword')

        response = self.client.post(reverse('changeInfoUser'), {
            'showName': '',
            'address': 'Ulica 2',
            'phoneNumber': '987654321',
            'currentPassword': '',
            'newPassword': '',
            'newPasswordSubmit': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'promenaInformacijaKorisnika.html')

        # Check if the user's information is updated in the database
        self.existingBuyer = Kupac.objects.get(email=self.existingBuyer.email)
        user = Kupac.objects.get(email=self.existingBuyer.email)
        self.assertEqual(self.existingBuyer.javnoime, 'Jane Smith')
        self.assertEqual(self.existingBuyer.adresa, 'Ulica 2')
        self.assertEqual(self.existingBuyer.brtelefona, '987654321')

    def test_change_user_info_invalid_password(self):
        user = Kupac.objects.get(email=self.existingBuyer.email)
        oldPass = 'testpassword'
        self.assertTrue(user.check_password(oldPass))
        self.client.login(email=self.existingBuyer.email, password=oldPass)

        response = self.client.post(reverse('changeInfoUser'), {
            'showName': '',
            'address': '',
            'phoneNumber': '',
            'currentPassword': 'wrongpassword',
            'newPassword': 'newpassword',
            'newPasswordSubmit': 'newpassword',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'promenaInformacijaKorisnika.html')

        # Check if the user's information is updated in the database
        user = Kupac.objects.get(email=self.existingBuyer.email)
        self.assertTrue(user.check_password(oldPass))  # Assert that the password is not updated

    def test_reset_password(self):
        oldPass = 'testpassword'
        user = Kupac.objects.get(email=self.existingBuyer.email)
        self.assertTrue(user.check_password(oldPass))

        response = self.client.post(reverse('resetPassword'), {
            'email': self.existingBuyer.email,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Check if the user's password is updated in the database and email is sent
        user = Kupac.objects.get(email=self.existingBuyer.email)
        self.assertFalse(user.check_password(oldPass))  # Assert that the password is updated
