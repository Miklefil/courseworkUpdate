from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "avatar", "verification")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()


# class VerificationForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ("verification_code", )

class VerificationForm(forms.Form):
    verification_code = forms.CharField(max_length=4, label='Verification Code')