import logging
from datetime import datetime, timedelta

from django.utils import timezone
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing.models import Mailing, LogMailing
from mailing.services import send_email_to_clients

logger = logging.getLogger(__name__)


def my_job():
    current_time = datetime.utcnow()
    current_date = datetime.utcnow().date()
    for mailing_settings in Mailing.objects.filter(status=Mailing.STATUS_STARTED):

        start_date = datetime.combine(current_date, mailing_settings.start_time)
        current_stop_date = datetime.combine(current_date, mailing_settings.end_time)
        stop_date = current_stop_date if mailing_settings.end_time > mailing_settings.start_time else (current_stop_date
                                                                                                       + timedelta
                                                                                                       (hours=24))
        if start_date < current_time < stop_date:

            #client_mailing = mailing_settings.clientmailing_set.all()
             #for _ in range(0):
             #for client in client_mailing:
            logs = LogMailing.objects.filter(
                settings=mailing_settings,
            )

            if logs.exists():
                last_try_date = LogMailing.objects.filter(settings=mailing_settings).order_by('-last_mailing').first()

                if mailing_settings.period == Mailing.PERIOD_DAILY:
                    if (current_time - last_try_date).days >= 1:
                        send_email_to_clients(mailing_settings)
                        # send_mailing(mailing_settings, client)

                elif mailing_settings.mailing_period == Mailing.PERIOD_WEEKLY:
                    if (current_time - last_try_date).days >= 7:
                        # send_mailing(mailing_settings, client)
                        send_email_to_clients(mailing_settings)

                elif mailing_settings.mailing_period == Mailing.PERIOD_MONTHLY:

                    if (current_time - last_try_date).days >= 30:
                        send_email_to_clients(mailing_settings)
                        # send_mailing(mailing_settings, client)

            else:
                send_email_to_clients(mailing_settings)
                # send_mailing(mailing_settings, client)


# def my_job():
#     now = timezone.now()
#
#     for mailing_setting in Mailing.objects.filter(status=Mailing.STATUS_STARTED):
#         last_attempt = LogMailing.objects.filter(settings=mailing_setting).order_by('-last_mailing').first()
#
#         if last_attempt:
#             last_attempt_date = last_attempt.last_mailing
#             time_difference = now - last_attempt_date
#
#             if mailing_setting.period == Mailing.PERIOD_DAILY and time_difference.days >= 1:
#                 next_send_time = last_attempt_date + timezone.timedelta(days=1, hours=mailing_setting.time.hour,
#                                                                         minutes=mailing_setting.time.minute)
#                 if now >= next_send_time:
#                     send_email_to_clients(mailing_setting)
#                     logger.info(f"Email sent to clients for MailingSettings {mailing_setting.id}")
#
#             elif mailing_setting.period == Mailing.PERIOD_WEEKLY and time_difference.days >= 7:
#                 next_send_time = last_attempt_date + timezone.timedelta(weeks=1, hours=mailing_setting.time.hour,
#                                                                         minutes=mailing_setting.time.minute)
#                 if now >= next_send_time:
#                     send_email_to_clients(mailing_setting)
#                     logger.info(f"Email sent to clients for MailingSettings {mailing_setting.id}")
#
#             elif mailing_setting.period == Mailing.PERIOD_MONTHLY and time_difference.days >= 30:
#                 next_send_time = last_attempt_date + timezone.timedelta(days=30, hours=mailing_setting.time.hour,
#                                                                         minutes=mailing_setting.time.minute)
#                 if now >= next_send_time:
#                     send_email_to_clients(mailing_setting)
#                     logger.info(f"Email sent to clients for MailingSettings {mailing_setting.id}")
#
#         else:
#             send_time = timezone.datetime(now.year, now.month, now.day, mailing_setting.time.hour,
#                                           mailing_setting.time.minute, tzinfo=timezone.get_current_timezone())
#             if now >= send_time:
#                 send_email_to_clients(mailing_setting)
#                 logger.info(f"Email sent to clients for MailingSettings {mailing_setting.id}")


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
