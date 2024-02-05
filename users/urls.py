from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, ProfileDetailView, verification, verify_code

app_name = UsersConfig.name

urlpatterns = [


    path("", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", RegisterView.as_view(), name="registration"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("detail/", ProfileDetailView.as_view(), name="detail"),

    path('verification/', verification, name='verification'),
    path('verify_code/<str:code>/', verify_code, name='verify_code'),

]
