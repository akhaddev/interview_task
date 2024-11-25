from django.db import models
from ..common.models import BaseModel, BaseMeta
from ..menu.models import Menu
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



class Order(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    menu_items = models.ManyToManyField(Menu)
    total_price = models.DecimalField(max_digits=25, decimal_places=2, default=0.0)


    class Meta(BaseMeta):
        verbose_name = 'Order'
        verbose_name_plural = 'Orders' 

    def __str__(self):
        return f"Order {self.id}"
    


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    

    class Meta(BaseMeta):
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems' 

    def __str__(self):
        return f"Order Item {self.id}"




# MongoDB

class MongoOrder(models.Model):
    postgres_id = models.IntegerField(unique=True)
    user_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=25, decimal_places=2, default=0.0)
    menu_items = models.ManyToManyField(Menu)


class MongoOrderItem(models.Model):
    postgres_id = models.IntegerField(unique=True)
    order_id = models.IntegerField()
    menu_item_id = models.IntegerField()
    quantity = models.PositiveIntegerField(default=0)



@receiver(post_save, sender=Order)
def sync_order_to_mongo(sender, instance, **kwargs):
    mongo_order, created = MongoOrder.objects.update_or_create(
        postgres_id=instance.id,
        defaults={
            'user_id': instance.user.id if instance.user else None,
            'total_price': str(instance.total_price),
        }
    )    
    mongo_order.menu_items.set([menu.id for menu in instance.menu_items.all()])


@receiver(post_delete, sender=Order)
def delete_order_from_mongo(sender, instance, **kwargs):
    MongoOrder.objects(postgres_id=instance.id).delete()


@receiver(post_save, sender=OrderItem)
def sync_order_item_to_mongo(sender, instance, **kwargs):
    MongoOrderItem.objects.update_or_create(
        postgres_id=instance.id,
        defaults={
            'order_id': instance.order.id,
            'menu_item_id': instance.menu_item.id,
            'quantity': instance.quantity,
        }
    )

@receiver(post_delete, sender=OrderItem)
def delete_order_item_from_mongo(sender, instance, **kwargs):
    MongoOrderItem.objects(postgres_id=instance.id).delete()