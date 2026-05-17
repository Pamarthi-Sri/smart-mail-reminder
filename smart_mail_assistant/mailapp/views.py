from django.shortcuts import render

# Create your views here.
from .gmail_reader import read_emails


def home(request):
    mails = read_emails()

    return render(request, 'home.html', {
        'mails': mails
    })