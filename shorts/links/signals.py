from .models import Link
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.core.cache import cache


@receiver(signal=[pre_save, pre_delete], sender=Link)
def invalidate_link_cache(sender, instance, *args):
    cache_key = instance.short_link
    cache.delete(cache_key)
