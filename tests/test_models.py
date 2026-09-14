from django.core.exceptions import ValidationError
from django.test import TestCase
from common.validators import validate_bd_phone

class ValidatorTests(TestCase):
    def test_accepts_bd_mobile(self): validate_bd_phone("+8801712345678")
    def test_rejects_non_bd_mobile(self):
        with self.assertRaises(ValidationError): validate_bd_phone("12345")
