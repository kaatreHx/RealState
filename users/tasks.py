from celery import shared_task
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage

@shared_task
def send_welcome_email(user_email, otp):
    email = EmailMessage(
        subject='Welcome to RealState! Verify Your Account',
        body=f"""
            Hello,

            Thank you for registering with RealState, your trusted platform for property listings and rentals.
            To complete your registration, please verify your email address using the following One-Time Password (OTP):

            Your OTP: {otp}

            If you did not sign up for a RealState account, please ignore this email.

            Best regards,
            The RealState Team
            """,
        from_email='bobmagarketa@gmail.com',
        to=[user_email],
    )
    email.send()