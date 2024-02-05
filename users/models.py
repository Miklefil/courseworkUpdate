from django.contrib.auth.models import AbstractUser
from django.db import models
import random


class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/", verbose_name="Avatar", null=True, blank=True)

    username = None
    email = models.EmailField(unique=True, verbose_name="Mail")
    verification = models.BooleanField(default=False, verbose_name="Verification")
    verification_code = models.CharField(max_length=4, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def generate_verification_code(self):

        code = ''.join([str(int(random.random() * 10)) for _ in range(4)])
        self.verification_code = code
        return code


    def verify(self, entered_code):

        if self.verification_code == entered_code:
            self.verification = True
            self.save()
            return True
        return False
