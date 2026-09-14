from django.core.mail import send_mail
def send_verification(email,token): send_mail("Confirm subscription",f"Verification token: {token}",None,[email])
