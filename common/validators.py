import re
from pathlib import Path
from django.core.exceptions import ValidationError

BD_PHONE = re.compile(r"^(?:\+?880|0)1[3-9]\d{8}$")

def validate_bd_phone(value):
    if not BD_PHONE.fullmatch(value.replace(" ", "").replace("-", "")):
        raise ValidationError("Enter a valid Bangladesh mobile number.")

def validate_upload(value, *, extensions, max_mb=10):
    if Path(value.name).suffix.lower().lstrip(".") not in extensions:
        raise ValidationError(f"Allowed extensions: {', '.join(sorted(extensions))}.")
    if value.size > max_mb * 1024 * 1024:
        raise ValidationError(f"File must be no larger than {max_mb} MB.")

def validate_image(value):
    validate_upload(value, extensions={"jpg", "jpeg", "png", "webp"}, max_mb=8)

def validate_pdf(value):
    validate_upload(value, extensions={"pdf"}, max_mb=10)

def validate_cv(value):
    validate_upload(value, extensions={"pdf", "doc", "docx"}, max_mb=5)
