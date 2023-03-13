from django.urls import path

from .views import MessageToAdminView, MessageFromAdmin

urlpatterns = [
    path('message_to_admin/', MessageToAdminView.as_view(), name='message_to_admin'),
    path('message_from_admin/<int:pk>/', MessageFromAdmin.as_view(),
         name='message_from_admin')
]
