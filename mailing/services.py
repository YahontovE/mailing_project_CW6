import datetime
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import LogMailing
import logging

logger = logging.getLogger(__name__)


def send_email_to_clients(mailing_settings):
    message_mail=mailing_settings.messagemailing_set.first()
    clients = mailing_settings.client.all()
    clients_list = [client.email for client in clients]

    answer_mail_server = None
    status = LogMailing.STATUS_FAILD

    try:
        letter = send_mail(
            subject=message_mail.title,  #mailing_settings.message.title
            message=message_mail.body,  #mailing_settings.message.body
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=clients_list,
        )

        if letter:
            status = LogMailing.STATUS_OK
            answer_mail_server = True

    except SMTPException as e:
        answer_mail_server = False
        logger.error(f"SMTPException occurred: {e}")
    else:
        logger.info("Email sent successfully")

    if answer_mail_server:
        logger.info(f"Server response: {answer_mail_server}")

    LogMailing.objects.create(
        status_try=status,
        settings=mailing_settings,
        answer_mail_server=answer_mail_server
    )