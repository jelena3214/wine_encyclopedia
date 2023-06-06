from django.apps import AppConfig

"""
    Author: Jelena Cvetic 2020/0305
    Django application setup.
"""


class UserappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userApp'
