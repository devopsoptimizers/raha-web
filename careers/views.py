from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from common.mixins import AuditActorMixin
from common.permissions import IsContentAdmin
from common.throttles import PublicFormThrottle
from .models import Job, JobApplication
from .serializers import JobApplicationAdminSerializer, JobApplicationSerializer, JobSerializer
class JobViewSet(AuditActorMixin,viewsets.ModelViewSet):
    serializer_class=JobSerializer; permission_classes=[IsContentAdmin]; filterset_fields=("department","job_type","location","is_published"); search_fields=("title","description")
    def get_queryset(self):
        qs=Job.objects.all(); return qs if self.request.user.is_authenticated else qs.filter(is_published=True)
    @action(detail=False,url_path="slug/(?P<slug>[-a-zA-Z0-9_]+)")
    def by_slug(self,request,slug=None): return Response(self.get_serializer(self.get_queryset().get(slug=slug)).data)
    @action(detail=True,methods=["post"],permission_classes=[AllowAny],throttle_classes=[PublicFormThrottle])
    def apply(self,request,pk=None):
        data=request.data.copy(); data["job"]=self.get_object().pk; s=JobApplicationSerializer(data=data); s.is_valid(raise_exception=True); s.save(); return Response(s.data,status=201)
class JobApplicationViewSet(AuditActorMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset=JobApplication.objects.select_related("job"); serializer_class=JobApplicationAdminSerializer; permission_classes=[IsContentAdmin]; filterset_fields=("job","status")
    @action(detail=True,methods=["patch"])
    def status(self,request,pk=None):
        obj=self.get_object(); s=self.get_serializer(obj,data=request.data,partial=True); s.is_valid(raise_exception=True); self.perform_update(s); return Response(s.data)
