from urllib.parse import urlsplit
from django.conf import settings


class PublicOriginMiddleware:
    """Use the browser-facing origin when serializers build absolute media URLs."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.origin = urlsplit(settings.PUBLIC_API_ORIGIN) if settings.PUBLIC_API_ORIGIN else None

    def __call__(self, request):
        if self.origin and request.get_host().split(":", 1)[0] in {"web", "backend"}:
            request.META["HTTP_HOST"] = self.origin.netloc
            request.META["HTTP_X_FORWARDED_PROTO"] = self.origin.scheme
        return self.get_response(request)
