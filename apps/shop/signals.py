from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import fashionMallSKUSpecs


@receiver(pre_save, sender=fashionMallSKUSpecs)
def sku_specs_pre_save(sender, instance, **kwargs):
    """
    SPU保存前
    """
    print(sender, instance, kwargs)
    