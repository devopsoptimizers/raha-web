from django.utils import timezone
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from common.permissions import IsContentAdmin
from common.mixins import AuditActorMixin
from .models import NewsletterIssue, Subscriber
from .tasks import send_verification
class NewsletterEmailSerializer(serializers.Serializer): email=serializers.EmailField()
class TokenSerializer(serializers.Serializer): token=serializers.CharField()
class SubscriberSerializer(serializers.ModelSerializer):
    class Meta: model=Subscriber; fields=("id","email","is_verified","created_at","unsubscribed_at")
class NewsletterIssueSerializer(serializers.ModelSerializer):
    class Meta: model=NewsletterIssue; fields="__all__"; read_only_fields=("created_by","updated_by")
class NewsletterIssueViewSet(AuditActorMixin, viewsets.ModelViewSet):
    queryset=NewsletterIssue.objects.all(); serializer_class=NewsletterIssueSerializer
    search_fields=("title","issue_number"); filterset_fields=("is_active",)
    def get_permissions(self):
        return [AllowAny()] if self.action in ("list","retrieve") else [IsContentAdmin()]
    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(is_active=True) if not self.request.user.is_authenticated else queryset
@extend_schema(request=NewsletterEmailSerializer,responses={202:None})
@api_view(["POST"])
@permission_classes([AllowAny])
def subscribe(request):
    s=NewsletterEmailSerializer(data=request.data); s.is_valid(raise_exception=True); obj,_=Subscriber.objects.get_or_create(email=s.validated_data["email"].lower()); obj.is_active=True; obj.unsubscribed_at=None; obj.save(); send_verification(obj.email,obj.verification_token); return Response({"detail":"Check your email to verify."},status=202)
@extend_schema(request=TokenSerializer,responses={200:None})
@api_view(["POST"])
@permission_classes([AllowAny])
def verify(request):
    s=TokenSerializer(data=request.data); s.is_valid(raise_exception=True); obj=Subscriber.objects.get(verification_token=s.validated_data["token"]); obj.is_verified=True; obj.save(update_fields=["is_verified","updated_at"]); return Response({"detail":"Subscription verified."})
@extend_schema(request=NewsletterEmailSerializer,responses={204:None})
@api_view(["POST"])
@permission_classes([AllowAny])
def unsubscribe(request):
    s=NewsletterEmailSerializer(data=request.data); s.is_valid(raise_exception=True); Subscriber.objects.filter(email=s.validated_data["email"].lower()).update(is_active=False,unsubscribed_at=timezone.now()); return Response(status=204)
@extend_schema(responses=SubscriberSerializer(many=True))
@api_view(["GET"])
@permission_classes([IsContentAdmin])
def subscribers(request): return Response(SubscriberSerializer(Subscriber.objects.all(),many=True).data)
