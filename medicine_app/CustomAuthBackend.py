from django.contrib.auth.backends import BaseBackend
from medicine_app.models import CreateUser

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = CreateUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CreateUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CreateUser.objects.get(pk=user_id)
        except CreateUser.DoesNotExist:
            return None