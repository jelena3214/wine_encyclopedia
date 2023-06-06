from django.contrib.auth.decorators import user_passes_test

"""
    Author: Jelena Cvetic 2020/0305
    Custom function decorators for checking if user is in the specific group and if user is not registered.
"""


def group_required(*group_names):
    def in_groups(user):
        if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
            return True
        return False

    return user_passes_test(in_groups, login_url='/')


def notLoggedIn():
    def loggedIn(user):
        return not user.is_authenticated

    return user_passes_test(loggedIn, login_url='/')
