from django.core.exceptions import ValidationError
from django.db import models
from common.models import TimeStampedUUIDModel
from common.validators import validate_image
class SiteSettings(TimeStampedUUIDModel):
    company_name=models.CharField(max_length=180); logo=models.ImageField(upload_to="settings/",blank=True,validators=[validate_image]); favicon=models.ImageField(upload_to="settings/",blank=True,validators=[validate_image]); hotline=models.CharField(max_length=30,blank=True); email=models.EmailField(blank=True); office_address=models.TextField(blank=True); google_maps_url=models.URLField(blank=True); business_hours=models.CharField(max_length=200,blank=True); social_links=models.JSONField(default=dict,blank=True); footer_content=models.TextField(blank=True); default_seo_title=models.CharField(max_length=70,blank=True); default_seo_description=models.CharField(max_length=170,blank=True); google_analytics_id=models.CharField(max_length=50,blank=True); google_tag_manager_id=models.CharField(max_length=50,blank=True); facebook_pixel_id=models.CharField(max_length=50,blank=True)
    footer_explore_title=models.CharField(max_length=80,blank=True); footer_contact_title=models.CharField(max_length=80,blank=True); footer_copyright_text=models.CharField(max_length=250,blank=True)
    footer_link_1_label=models.CharField(max_length=80,blank=True); footer_link_1_url=models.CharField(max_length=300,blank=True)
    footer_link_2_label=models.CharField(max_length=80,blank=True); footer_link_2_url=models.CharField(max_length=300,blank=True)
    footer_link_3_label=models.CharField(max_length=80,blank=True); footer_link_3_url=models.CharField(max_length=300,blank=True)
    footer_link_4_label=models.CharField(max_length=80,blank=True); footer_link_4_url=models.CharField(max_length=300,blank=True)
    contact_hero_label=models.CharField(max_length=100,blank=True); contact_hero_title=models.CharField(max_length=160,blank=True); contact_hero_image=models.ImageField(upload_to="settings/contact/",blank=True,validators=[validate_image])
    contact_details_label=models.CharField(max_length=100,blank=True); contact_details_title=models.CharField(max_length=200,blank=True)
    contact_form_label=models.CharField(max_length=100,blank=True); contact_form_title=models.CharField(max_length=160,blank=True)
    contact_image_label=models.CharField(max_length=100,blank=True); contact_image_title=models.CharField(max_length=200,blank=True); contact_form_image=models.ImageField(upload_to="settings/contact/",blank=True,validators=[validate_image])
    contact_map_embed_url=models.URLField(blank=True)
    contact_map_button_label=models.CharField(max_length=80,blank=True)
    contact_name_label=models.CharField(max_length=80,blank=True); contact_phone_label=models.CharField(max_length=80,blank=True); contact_email_label=models.CharField(max_length=80,blank=True)
    contact_user_type_label=models.CharField(max_length=80,blank=True); contact_client_label=models.CharField(max_length=80,blank=True); contact_landowner_label=models.CharField(max_length=80,blank=True)
    contact_message_label=models.CharField(max_length=80,blank=True); contact_submit_label=models.CharField(max_length=80,blank=True)
    def clean(self):
        if not self.pk and SiteSettings.objects.exists(): raise ValidationError("Only one site settings record is allowed.")
