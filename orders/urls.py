from django.urls import path

from . import views


urlpatterns = [

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'add/<int:biscuit_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'update/<int:item_id>/',
        views.update_cart,
        name='update_cart'
    ),

    path(
        'remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'success/',
        views.order_success,
        name='order_success'
    ),

    path(
        'myorders/',
        views.my_orders,
        name='myorders'
    ),
]