from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Supply, Notification

@receiver(post_save, sender=Product)
def notify_new_product(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.created_by,
            message=f"Добавлен новый продукт: {instance.name}"
        )

@receiver(post_save, sender=Supply)
def notify_new_supply(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.created_by,
            message=f"Создана новая поставка #{instance.id}"
        )

@receiver(post_save, sender=Product)
def check_stock_level(sender, instance, **kwargs):
    if instance.quantity < 10:
        Notification.objects.create(
            user=instance.created_by,
            message=f"Внимание: низкий запас продукта {instance.name} (осталось {instance.quantity})"
        )
