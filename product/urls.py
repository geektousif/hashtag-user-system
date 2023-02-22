from django.urls import path

from .views import ProductDetailView, ProductSearchList
from order.views import AddOrderItem


urlpatterns = [
    # path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/add_order/', AddOrderItem.as_view(), name='add_order_item'),
    path("", ProductSearchList.as_view(), name='product_search'),


]
