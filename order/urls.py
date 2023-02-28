from django.urls import path

from .views import ProductsInCart, PlaceOrder, RemoveOrderItem

urlpatterns = [
    path('cart/', ProductsInCart.as_view(), name='cart_list'),
    path('place_order/', PlaceOrder.as_view(), name='place_order'),
    path('remove_item/<int:pk>/', RemoveOrderItem.as_view(), name='remove_cart_item')
]
