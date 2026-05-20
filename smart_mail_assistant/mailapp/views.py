from django.http import HttpResponse
from .gmail_reader import read_emails

def home(request):

    try:
        mails = read_emails()

        if mails:
            return HttpResponse(
                "Important mails found:<br><br>" +
                "<br>".join(mails)
            )

        else:
            return HttpResponse(
                "No important unread mails found."
            )

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")