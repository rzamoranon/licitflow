from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_on_user_create(sender, instance, created, **kwargs):
    if created:
        # Evita duplicados si ya existe
        UserProfile.objects.get_or_create(user=instance)
