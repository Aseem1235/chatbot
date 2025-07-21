from django.contrib.auth.backends import BaseBackend

from .models import LoginDetails
class LoginDetailsBackend(BaseBackend):
    def authenticate(self,request,username=None,password=None):
        try:
            user = LoginDetails.objects.get(username=username)
            if user.password==password:
                return user
        except LoginDetails.DoesNotExist:
            return None
    def get_user(self,user_id):
        try:
            return LoginDetails.objects.get(pk=user_id)
        except LoginDetails.DoesNotExist:
            return None