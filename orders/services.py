from django.core.mail import send_mail

from robots.models import Robot
from .models import Order


def find_model_in_stock(serial):
    robot = Robot.objects.filter(serial=serial).order_by("created").first()
    return robot if robot else None


def update_stocks(robot_id):
    Robot.objects.filter(id=robot_id).delete()


def get_pending_orders():
    return Order.objects.select_related("customer").filter(status="Pending")


def send_email_notification(recipients, robot_model, robot_version):
    subject = "Модель по вашему заказу появилась в наличии"
    message = "Добрый день!\n\n" \
        f"Недавно вы интересовались нашим роботом модели {robot_model}, версии {robot_version}.\n" \
        "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"

    from_ = "r4c_customer_service@gmail.com"

    send_mail(subject, message, recipient_list=recipients, from_email=from_)
