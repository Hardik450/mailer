from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import threading


# Thread class to handle async email sending
class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.message,
            settings.DEFAULT_FROM_EMAIL,
            [self.recipient_list],
            fail_silently=False,
        )


@api_view(['POST'])
def send_email(request):
    """
    API endpoint to send an email asynchronously.
    Expects 'subject', 'message', and 'recipient_list' in POST data.
    """
    print("DEBUG incoming data:", request.data)
    subject = request.data.get('subject')
    message = request.data.get('message')
    recipient_list = request.data.get('recipient_list')

    if not subject or not message or not recipient_list:
        return Response(
            {"error": "Subject, message, and recipient_list are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Start email sending in a background thread
        EmailThread(subject, message, recipient_list).start()

        return Response(
            {"success": "Email is being sent in the background."},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        print("Error sending email:", e)
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def home(request):
    return render(request, 'index.html')
