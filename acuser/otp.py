import pyotp
from datetime import datetime, timedelta
from django.core.mail import EmailMessage

def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_key'] = totp.secret
    otp_valid = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid'] = otp_valid.strftime('%Y-%m-%d %H:%M:%S')
    print(f"Your otp is {otp}")

    mail = request.session['mail']
    subject = 'Verify your Account'
    message = f'Your OTP is {otp}'
    from_email = 'm.gouse7736@example.com'
    recipient_email = [mail]

    try:
        email = EmailMessage(subject, message, from_email, recipient_email)
        email.send()
    except Exception as e:
        print(f"Failed to send OTP email: {str(e)}")

