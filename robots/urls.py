from django.urls import path

from . import views


urlpatterns = [
    path("v1/robots/new/", views.AddRobotAPI.as_view(), name="add_robot_api"),
]
