from rest_framework.throttling import AnonRateThrottle


class PublicFormThrottle(AnonRateThrottle):
    scope = "public_form"
