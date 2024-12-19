from django.db.models.signals import post_save
from django.dispatch import receiver

from robots.models import Robot
from .models import Order
from .services import find_model_in_stock, update_stocks, get_pending_orders
from .tasks import send_email_notification


@receiver(post_save, sender=Order)
def update_order_status(sender, instance, created, **kwargs):
    """
    Сигнал обновляет статус заказа на 'Выполнен' в случае,
    если нужный робот в наличии
    """
    if created:
        target_robot = find_model_in_stock(instance.robot_serial)
        if target_robot:
            instance.status = "Completed"
            update_stocks(target_robot.id)
        
        # Сохранение изменений в базе данных
        instance.save(update_fields=["status"])


@receiver(post_save, sender=Robot)
def send_appeared_in_stock_notification(sender, instance, created, **kwargs):
    """
    Сигнал отправляет email пользователю, когда робот по его заказу появляется в наличии
    """
    if created:
        pending_orders = get_pending_orders()
        recipients = [order.customer.email for order in pending_orders if order.robot_serial == instance.serial]
        send_email_notification.delay(recipients, instance.model, instance.version)
