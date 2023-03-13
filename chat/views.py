from django.shortcuts import render
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .models import Message
from .serializers import MessageSerializer
# Create your views here.


class MessageToAdminView(ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Message.objects.filter(
            Q(sender=self.request.user) | Q(reciever=self.request.user)).order_by('-message_time')
        if isinstance(queryset, QuerySet):
            queryset = queryset.all().order_by('-message_time')
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data['sender'] = self.request.user.id
        serializer.initial_data['reciever'] = get_user_model(
        ).objects.get(is_superuser=True).id
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class MessageFromAdmin(ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Message.objects.filter(
            Q(sender=self.request.user, reciever=pk) | Q(sender=pk, reciever=self.request.user)).order_by('-message_time')
        if isinstance(queryset, QuerySet):
            queryset = queryset.all().order_by('-message_time')
        return queryset

    def create(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data['sender'] = self.request.user.id
        serializer.initial_data['reciever'] = pk
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
