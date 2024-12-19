from django.core.mail import send_mail

from .celery import app


@app.task
def send_email_notification(recipients, robot_model, robot_version):
    subject = "Модель по вашему заказу появилась в наличии"
    message = "Добрый день!\n\n" \
        f"Недавно вы интересовались нашим роботом модели {robot_model}, версии {robot_version}.\n" \
        "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"

    from_ = "r4c_customer_service@gmail.com"

    send_mail(subject, message, recipient_list=recipients, from_email=from_)

