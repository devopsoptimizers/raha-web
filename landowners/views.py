from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from common.mixins import AuditActorMixin
from common.permissions import IsSalesOfficer
from common.throttles import PublicFormThrottle
from .models import LandownerProposal
from .serializers import LandownerAdminSerializer, LandownerPublicSerializer
class LandownerProposalViewSet(AuditActorMixin,viewsets.ModelViewSet):
    throttle_classes=[PublicFormThrottle]
    queryset=LandownerProposal.objects.select_related("division","district","area","assigned_to").prefetch_related("documents"); filterset_fields=("status","assigned_to","division","district","area")
    search_fields=("owner_name","phone","email","land_address","ownership_type","message")
    def get_permissions(self): return [AllowAny()] if self.action=="create" else [IsSalesOfficer()]
    def get_serializer_class(self): return LandownerPublicSerializer if self.action=="create" else LandownerAdminSerializer
    @action(detail=True,methods=["patch"])
    def status(self,request,pk=None): return self._patch(request,{"status":request.data.get("status")})
    @action(detail=True,methods=["patch"])
    def assign(self,request,pk=None): return self._patch(request,{"assigned_to":request.data.get("assigned_to")})
    def _patch(self,request,data):
        obj=self.get_object(); s=self.get_serializer(obj,data=data,partial=True); s.is_valid(raise_exception=True); self.perform_update(s); return Response(s.data)
