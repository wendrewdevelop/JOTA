from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from jota.permissions import IsAdminPermission, IsEditorOrReadOnly, IsReader
from .models import News
from .serializers import NewsSerializer


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all().order_by('-published_at')
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminPermission(), IsEditorOrReadOnly()]
        return [IsReader()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return News.objects.all().order_by(
                '-published_at'
            )
        elif user.is_writer:
            return News.objects.filter(
                author=user
            ).order_by('-published_at')
        elif user.is_reader:
            return News.objects.filter(
                plan=user.plan_name
            ).order_by('-published_at')
        return News.objects.none()

    def list(self, request, *args, **kwargs):
        user = request.user
        print(f'User: {user}, Authenticated: {user.is_authenticated}, Plan: {user.plan_name}')
        if user.is_authenticated:
            user_plan = user.plan_name
            queryset = self.get_queryset().filter(
                plan=user_plan
            )
        else:
            queryset = self.get_queryset().filter(
                plan='info'
            )
        serializer = self.get_serializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Se 'post_image' não estiver em request.data, mantém o valor atual
        if not request.data.get('post_image'):
            request.data._mutable = True  # só se for QueryDict
            request.data['post_image'] = instance.post_image

        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
