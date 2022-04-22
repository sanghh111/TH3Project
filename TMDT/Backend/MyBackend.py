import re
from django.contrib.auth.backends import BaseBackend

from TMDT.models import User


class MyBackEnd(BaseBackend):
    #authenticate trả về 1 object nếu credentials is valid
    def authenticate(self, request , email=None , password= None ):
        try:
            user = (User.objects.get(email = email))
            valid_password  = (user.password == password )
            if valid_password:
                return user
            else :
                return None
        except User.DoesNotExist:
            return None