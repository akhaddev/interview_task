from django.db import models
from ..common.models import BaseModel, BaseMeta
from django.conf import settings
from ..menu.models import Menu
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



class Cart(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)


    class Meta(BaseMeta):
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts' 

    def __str__(self):
        return self.user.username
    


# MongoDB

class MongoCart(models.Model):
    postgres_id = models.IntegerField(unique=True)
    user_id = models.IntegerField()
    menu_item_id = models.IntegerField()
    quantity = models.PositiveIntegerField(default=0)



@receiver(post_save, sender=Cart)
def sync_cart_to_mongo(sender, instance, **kwargs):
    MongoCart.objects.update_or_create(
        postgres_id=instance.id,
        defaults={
            'user_id': instance.user.id,
            'menu_item_id': instance.menu_item.id if instance.menu_item else None,
            'quantity': instance.quantity,
        }
    )

@receiver(post_delete, sender=Cart)
def delete_cart_from_mongo(sender, instance, **kwargs):
    MongoCart.objects.filter(postgres_id=instance.id).delete()