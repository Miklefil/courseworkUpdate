from django.contrib import admin

from mailings.models import Client, Message, Settings, Log, Blog


# py manage.py createsuperuser UN:admin PW:12345
class MessageInline(admin.TabularInline):
    model = Message


class SettingsInline(admin.TabularInline):
    model = Settings


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname', 'comment')
    list_filter = ('name', 'surname')
    search_fields = ('email', 'name', 'surname')
    inlines = [MessageInline, SettingsInline]


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('mailing_time', 'periodicity', 'mailing_status')
    search_fields = ('mailing_time', 'periodicity', 'mailing_status')
    list_filter = ('mailing_time', 'periodicity', 'mailing_status')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')
    search_fields = ('subject', 'body')

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):

    list_display = ("client", "date_time", "status", "server_response", "email_subject", "email_body")

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    list_display = ("title", "number_of_view", "publication_date")



