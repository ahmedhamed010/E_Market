from django.urls import path
from . import views

urlpatterns = [
    path('order/new/' , views.new_order , name='new_order'),
    path('orders/all/' , views.get_all_orders , name='get_all_orders'),
    path('order/<str:pk>/' , views.get_order , name='get_order'),
    path('order/<str:pk>/process/' , views.update_order , name='update_order'),
    path('order/<str:pk>/delete/' , views.delete_order , name='delete_order'),
]
