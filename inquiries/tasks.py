from django.core.mail import send_mail
def send_inquiry_confirmation(email,reference):
    if email: send_mail("Inquiry received",f"Your inquiry reference is {reference}.",None,[email])
