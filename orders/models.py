from django.db import models

from customers.models import Customer


class Order(models.Model):
    status_choices = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    )
    
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5,blank=False, null=False)
    status = models.CharField(max_length=9, choices=status_choices, default="Pending")
