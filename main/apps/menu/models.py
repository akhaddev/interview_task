from django.db import models
from ..common.models import BaseModel, BaseMeta
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Menu(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.CharField(max_length=255)

    class Meta(BaseMeta):
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus' 

    def __str__(self):
        return self.name
    

class MenuQrCode(BaseModel):
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    class Meta(BaseMeta):
        verbose_name = 'MenuQrCode'
        verbose_name_plural = 'MenuQrCodes' 



# MongoDB
    
class MongoMenu(models.Model):
    postgres_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    class Meta:
        db_table = 'menu_mongo' 


@receiver(post_save, sender=Menu)
def sync_menu_to_mongo(sender, instance, **kwargs):
    MongoMenu.objects.update_or_create(
        postgres_id=instance.id,
        defaults={
            'name': instance.name,
            'description': instance.description,
            'price': str(instance.price),
            'tags': instance.tags,
            'qr_code': instance.qr_code.url if instance.qr_code else None,
        }
    )

@receiver(post_delete, sender=Menu)
def delete_menu_from_mongo(sender, instance, **kwargs):
    MongoMenu.objects.filter(postgres_id=instance.id).delete()
