from django.urls import path
from pizza_order_api.views import PizzaOrderViewSet, pizza_order_list, pizza_order_create, pizza_order_single

urlpatterns = [
    path('search', pizza_order_list, name='pizza_order_list'),
    path('create', pizza_order_create, name='pizza_order_create'),
    path('<str:pk>',  pizza_order_single, name='pizza_order_single')
]
