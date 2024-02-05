from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.views import index, send_email_to_client, success, no_success, homepage, BlogListView, BlogDetailView, \
    BlogUpdateView, BlogDeleteView, BlogCreateView
from django.contrib.auth.decorators import login_required

from mailings.views import ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, ClientCreateView
from mailings.views import MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, MessageCreateView
from mailings.views import SettingsListView, SettingsDetailView, SettingsUpdateView, SettingsDeleteView, \
    SettingsCreateView

urlpatterns = [
    path("", homepage),
    path("index/", index, name="index"),

    path("client_list_view/", ClientListView.as_view(), name='client_list_view'),
    path("client_detail/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client_update/<int:pk>/", login_required(ClientUpdateView.as_view()), name="client_update"),
    path("client_delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path("client_create/", login_required(ClientCreateView.as_view()), name="client_create"),

    path("message_list_view/", MessageListView.as_view(), name='message_list_view'),
    path("message_detail/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),

    path("settings_list_view/", SettingsListView.as_view(), name="settings_list_view"),
    path("settings_detail/<int:pk>/", SettingsDetailView.as_view(), name="settings_detail"),
    path("settings_update/<int:pk>/", SettingsUpdateView.as_view(), name="settings_update"),
    path("settings_delete/<int:pk>/", SettingsDeleteView.as_view(), name="settings_delete"),
    path("settings_create/", SettingsCreateView.as_view(), name="settings_create"),

    path('send_email/<int:client_id>/', send_email_to_client, name='send_email_to_client'),
    path("email_success/", success, name='success'),
    path("email_no_success/", no_success, name='no success'),

    # cache --- nezapomenout si spustit redis-server.exe
    # path("blog/", cache_page(60)(BlogListView.as_view()), name="blog"),
    path("blog/", BlogListView.as_view(), name="blog"),
    path("blog_create/", BlogCreateView.as_view(), name="blog_create"),
    path("blog_detail/<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
    path("blog_update/<int:pk>/", BlogUpdateView.as_view(), name="blog_update"),
    path("blog_delete/<int:pk>/", BlogDeleteView.as_view(), name="blog_delete"),

]
