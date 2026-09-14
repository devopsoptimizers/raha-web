from django.utils import timezone
from rest_framework import serializers
from .models import Job, JobApplication
class JobSerializer(serializers.ModelSerializer):
    class Meta: model=Job; fields="__all__"; read_only_fields=("created_by","updated_by","deleted_at")
class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta: model=JobApplication; fields="__all__"; read_only_fields=("created_by","updated_by","status","internal_notes")
    def validate_job(self, job):
        if not job.is_published or job.application_deadline < timezone.localdate(): raise serializers.ValidationError("Applications are closed for this job.")
        return job
class JobApplicationAdminSerializer(serializers.ModelSerializer):
    class Meta: model=JobApplication; fields="__all__"; read_only_fields=("created_by","updated_by")
