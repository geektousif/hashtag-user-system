from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, index, RegisterUserView, user_login, user_logout, UpdateProfileView

from product.views import ProductViewSet

router = routers.DefaultRouter()

# Admin accessible Viewsets
router.register(r'admin-api/users', UserViewSet)
router.register(r'admin-api/products', ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('home/', index, name='index'),
    path('login/', user_login, name="user_login"),
    path('logout/', user_logout, name="user_logout"),
    path('register_user/', RegisterUserView.as_view(), name="register_user"),
    path('update_profile/', UpdateProfileView.as_view(), name="update profile")
    # path('api-auth/', include('rest_framework.urls')),
]
