from celery import shared_task
import time
from apps.lib.loggers import AppLogger


@shared_task
def send_otp_sms_task(phone_number: str, code: str):
    """
    Asynchronous task to send OTP SMS to a user.
    """
    try:
        AppLogger.log_activity(f"Starting SMS delivery to {phone_number}")

        time.sleep(3)

        print(f"\n[CELERY] SMS SENT TO: {phone_number} | CODE: {code}\n")

        AppLogger.log_activity(f"SMS delivered successfully to {phone_number}")
        return True

    except Exception as e:
        AppLogger.log_activity(f"Failed to send SMS to {phone_number}: {str(e)}")
        return False
