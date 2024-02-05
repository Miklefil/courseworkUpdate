from django.db import models
from django.urls import reverse
from django.utils import timezone


# pip3 install psycopg2-binary
# py manage.py migrate
# py manage.py makemigrations


class Client(models.Model):
    email = models.EmailField(verbose_name="E-mail")
    name = models.CharField(max_length=64, verbose_name="Name")
    surname = models.CharField(max_length=64, verbose_name="Surname")
    comment = models.TextField(verbose_name="Comment")

    def __str__(self):
        return f"{self.name} {self.surname} --- {self.email}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ("email",)


class Message(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages', verbose_name="Client",
                               null=True)
    # pokud je odstraněn Client, měly by být odstraněny i všechny související zprávy v MailingMessage.

    subject = models.CharField(max_length=256, verbose_name="E-mail subject")
    body = models.TextField(verbose_name="E-mail body")

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class Settings(models.Model):
    PERIODICITY_CHOICES = [  # CapsLock
        ("daily", "Once a day"),  # Раз в день,
        ("weekly", "Once a week"),  # Раз в неделю,
        ("monthly", "Once a month")  # Рах в месяц.
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='settings', verbose_name="Client")

    start_date = models.DateField(verbose_name="Starting date", blank=True, null=True)
    mailing_time = models.TimeField(verbose_name="Mailing time", blank=True, null=True)
    periodicity = models.CharField(max_length=12, choices=PERIODICITY_CHOICES, verbose_name="Periodicity")
    mailing_status = models.CharField(max_length=24, verbose_name="Mailing status")

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"


class Log(models.Model):
    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("finished", "Finished")
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    date_time = models.DateTimeField(default=timezone.now, verbose_name="Date & Time")
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, verbose_name="Status")
    server_response = models.TextField(verbose_name="Server response")

    email_subject = models.CharField(max_length=256, verbose_name="Email Subject", blank=True, null=True)
    email_body = models.TextField(verbose_name="Email Body", blank=True, null=True)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"


class Blog(models.Model):
    title = models.CharField(max_length=64, verbose_name="Title")
    article = models.CharField(max_length=512, verbose_name="Article")
    image = models.ImageField(upload_to="blog/", verbose_name="Blog Image", null=True, blank=True)
    number_of_view = models.PositiveIntegerField(default=0, verbose_name="Number of Views")
    publication_date = models.DateField(verbose_name="Publication Date")

    def __str__(self):
        return f"{self.title}"


    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"



