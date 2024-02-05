import random

from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, VerificationForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/registration.html"

    def get_success_url(self):
        return reverse('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:profile')


class ProfileDetailView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'users/user_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


def verification(request):
    """
    Veritifikace:
    v modelu User přidat:     verification = models.BooleanField(default=False, verbose_name="Verification")
    verification_code = models.CharField(max_length=4, null=True, blank=True) + funkce na ověření
    urls:
        path('verification/', verification, name='verification'),
    path('verify_code/<str:code>/', verify_code, name='verify_code'),

    v html veritification musí být : <form method="post" action="{% url 'users:verify_code' user.verification_code %}">
    a dole <button type="submit">Verify</button> tím se zadaný kod odešele do fuckce: verify_code

    """
    user = request.user
    if not user.verification_code:
        user.generate_verification_code()
        user.save()
    # send_mail(
    #     "verification of your email ",
    #     f"Type in this code: {user.verification_code}",
    #     settings.EMAIL_HOST_USER,
    #     [request.user.email]
    # )

    form = VerificationForm()
    print(user.verification_code)
    return render(request, 'users/verification.html', {'user_email': user.email, 'form': form})


def verify_code(request, code):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            entered_code = str(form.cleaned_data['verification_code'])
            user = request.user
            print(f"Entered code: {entered_code}")
            print(f"User verification code: {user.verification_code}")

            if user.verify(entered_code):
                messages.success(request, 'Verification successful!')
                return redirect(reverse('users:detail'))
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
        else:
            messages.error(request, 'Form is not valid. Please try again.')

    return redirect(reverse('users:detail'))

