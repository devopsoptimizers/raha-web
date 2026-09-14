from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from testimonials.models import Testimonial
from .models import ContentBlock, Slider
@receiver([post_save,post_delete],sender=Slider)
@receiver([post_save,post_delete],sender=ContentBlock)
@receiver([post_save,post_delete],sender=Testimonial)
def invalidate_home(**kwargs): cache.delete("homepage:v1")
