from .models import Customer
from django.core.mail import send_mail
import time
from django.conf import settings
from celery import shared_task
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


CUSTOMER_BATCH_SIZE = 100


@shared_task(bind=True, max_retries=3)
def send_birthday_emails_task(self, batch_size=CUSTOMER_BATCH_SIZE):
    try:
        total_customers = Customer.objects.count()
        today = datetime.now().date()
        for offset in range(0, total_customers, batch_size):
            customers = Customer.objects.filter(
                birthday__day=today.day, birthday__month=today.month)[offset:offset+batch_size]
            for customer in customers:
                send_birthday_greeting_email.delay(
                    customer.name, customer.email)
            time.sleep(1)
    except Exception as e:
        print(f"Error occurred while sending birthday emails: {e}")
        logger.error(f"Error occurred while sending birthday emails: {e}")
        raise self.retry(exc=e, countdown=10 * 2 ** self.request.retries)


@shared_task(bind=True, max_retries=3)
def send_birthday_greeting_email(self, customer_name, customer_email):
    try:
        subject = 'Happy Birthday!'
        message = f"""Hello {customer_name}, \nHappy Birthday! Wishing you a day filled with joy,laughter, and special moments.
        \nMay this year bring you happiness and success all your endeavors. \nEnjoy your special day!"""

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = customer_email

        send_mail(
            subject,
            message,
            from_email,
            [to_email],
            fail_silently=False
        )
    except Exception as e:
        logger.error(
            f"Error occurred while sending email {customer_email}: {e}")
        raise self.retry(exc=e, countdown=10 * 2 ** self.request.retries)
