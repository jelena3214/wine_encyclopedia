from django.contrib.auth.backends import ModelBackend
from baza.models import *

"""
    Custom authentication model using email as primary key.
"""

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            print(email)
            user = Korisnik.objects.get(email=email)
        except Korisnik.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return Korisnik.objects.get(pk=user_id)
        except Korisnik.DoesNotExist:
            return None
