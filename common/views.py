from django.db import connection
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiTypes, extend_schema

@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    connection.ensure_connection()
    cache.set("health", "ok", 5)
    return Response({"status": "ok", "database": True, "cache": cache.get("health") == "ok"})

@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(["GET"])
@permission_classes([AllowAny])
def readiness(request):
    connection.ensure_connection()
    return Response({"status": "ready"})

@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(["GET"])
@permission_classes([AllowAny])
def liveness(request):
    return Response({"status": "alive"})
