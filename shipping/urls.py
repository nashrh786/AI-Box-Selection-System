from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_order, name="create_order"),
    path("recommend/<int:order_id>/", views.recommend, name="recommend"),
]