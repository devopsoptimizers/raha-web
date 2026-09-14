from django.db import models
from common.models import SoftDeleteModel, TimeStampedUUIDModel
from common.validators import validate_bd_phone, validate_cv

class Job(SoftDeleteModel):
    class Type(models.TextChoices): FULL_TIME="FULL_TIME","Full time"; PART_TIME="PART_TIME","Part time"; CONTRACT="CONTRACT","Contract"; INTERNSHIP="INTERNSHIP","Internship"
    title=models.CharField(max_length=180); slug=models.SlugField(max_length=200, unique=True); department=models.CharField(max_length=100); job_type=models.CharField(max_length=20,choices=Type.choices); location=models.CharField(max_length=150); vacancy_count=models.PositiveSmallIntegerField(default=1); required_experience=models.CharField(max_length=300,blank=True); educational_requirements=models.TextField(blank=True); responsibilities=models.TextField(); description=models.TextField(); salary_range=models.CharField(max_length=120,blank=True); application_deadline=models.DateField(db_index=True); is_published=models.BooleanField(default=False,db_index=True)
class JobApplication(TimeStampedUUIDModel):
    class Status(models.TextChoices): RECEIVED="RECEIVED","Received"; REVIEWING="REVIEWING","Reviewing"; SHORTLISTED="SHORTLISTED","Shortlisted"; REJECTED="REJECTED","Rejected"; HIRED="HIRED","Hired"
    job=models.ForeignKey(Job,on_delete=models.PROTECT,related_name="applications"); applicant_name=models.CharField(max_length=150); phone=models.CharField(max_length=20,validators=[validate_bd_phone]); email=models.EmailField(); years_of_experience=models.CharField(max_length=100); previous_organization=models.CharField(max_length=180); education_degree=models.CharField(max_length=180); education_institution=models.CharField(max_length=220); cover_letter=models.TextField(); cv=models.FileField(upload_to="careers/cv/",validators=[validate_cv]); status=models.CharField(max_length=20,choices=Status.choices,default=Status.RECEIVED,db_index=True); internal_notes=models.TextField(blank=True)
    class Meta: constraints=[models.UniqueConstraint(fields=["job","email"],name="unique_job_applicant_email")]
