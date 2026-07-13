from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Shot


@receiver(post_save, sender=Shot)
def invalidate_shots_cache_on_save(sender, instance, **kwargs):
    """Очищення кешу стрічки робіт при створенні або редагуванні."""
    cache.delete('shots_list_cache')


@receiver(post_delete, sender=Shot)
def invalidate_shots_cache_on_delete(sender, instance, **kwargs):
    """Очищення кешу стрічки робіт при видаленні."""
    cache.delete('shots_list_cache')

