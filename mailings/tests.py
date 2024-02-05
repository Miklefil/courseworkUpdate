import psycopg2
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse
import os

from mailings.models import Client

# Create your tests here.
