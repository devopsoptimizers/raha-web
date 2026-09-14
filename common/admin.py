from django.contrib import admin
from amenities.models import Amenity
from blogs.models import BlogCategory, BlogPost, Tag
from careers.models import Job, JobApplication
from content.models import ContentBlock, Slider, TeamMember
from inquiries.models import Inquiry, InquiryNote, MeetingRequest, PublicMessage
from landowners.models import LandownerProposal, ProposalDocument
from locations.models import Area, District, Division
from media_gallery.models import GalleryItem, ProgressImage
from newsletter.models import Subscriber
from projects.models import ConstructionProgress, Project, PropertyType
from properties.models import ApartmentType, Unit
from settings_app.models import SiteSettings
from testimonials.models import Testimonial

class ManagedAdmin(admin.ModelAdmin):
    list_per_page=50; readonly_fields=("id","created_at","updated_at","created_by","updated_by")
    def save_model(self,request,obj,form,change):
        if not change: obj.created_by=request.user
        obj.updated_by=request.user; super().save_model(request,obj,form,change)

for model in (Amenity,BlogCategory,BlogPost,Tag,Job,JobApplication,ContentBlock,Slider,TeamMember,Inquiry,InquiryNote,MeetingRequest,PublicMessage,LandownerProposal,ProposalDocument,Area,District,Division,GalleryItem,ProgressImage,Subscriber,ConstructionProgress,Project,PropertyType,ApartmentType,Unit,SiteSettings,Testimonial):
    admin.site.register(model,ManagedAdmin)
