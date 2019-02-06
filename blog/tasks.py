from celery import shared_task
from django.core.mail import EmailMessage, send_mass_mail




# function for mailing out all notifications
@shared_task
def massMessageSend(subject_line, message_text, recipient_list):
    message = (subject_line, message_text, 'from@example.com', recipient_list)
    send_mass_mail((message,), fail_silently=False)
    return print("Message sent")
