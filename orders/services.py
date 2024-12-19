from robots.models import Robot
from .models import Order


def find_model_in_stock(serial):
    robot = Robot.objects.filter(serial=serial).order_by("created").first()
    return robot if robot else None


def update_stocks(robot_id):
    Robot.objects.filter(id=robot_id).delete()


def get_pending_orders():
    return Order.objects.select_related("customer").filter(status="Pending")
