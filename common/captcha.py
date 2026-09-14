import json
from urllib import parse, request
from django.conf import settings
from rest_framework import serializers


def validate_captcha(token, remote_ip=None):
    """Validate a Cloudflare Turnstile token when CAPTCHA is configured."""
    secret = settings.CAPTCHA_SECRET
    if not secret:
        return
    if not token:
        raise serializers.ValidationError("Please complete the CAPTCHA verification.")
    payload = {"secret": secret, "response": token}
    if remote_ip:
        payload["remoteip"] = remote_ip
    try:
        req = request.Request(
            settings.CAPTCHA_VERIFY_URL,
            data=parse.urlencode(payload).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode())
    except Exception as exc:
        raise serializers.ValidationError("CAPTCHA verification is temporarily unavailable.") from exc
    if not result.get("success"):
        raise serializers.ValidationError("CAPTCHA verification failed. Please try again.")


class CaptchaSerializerMixin:
    captcha_token = serializers.CharField(required=False, write_only=True, allow_blank=True)

    def validate_captcha_token(self, value):
        django_request = self.context.get("request")
        remote_ip = django_request.META.get("REMOTE_ADDR") if django_request else None
        validate_captcha(value, remote_ip)
        return value

    def create(self, validated_data):
        validated_data.pop("captcha_token", None)
        return super().create(validated_data)
