import random
import string
import httpx
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import login
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle
from rest_framework.generics import GenericAPIView
from users.models import User
from users.serializers import UserSerializer, CustomJWTAuthSerializer


class UserViewset(ModelViewSet):
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'user_individual'
    serializer_class = UserSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'POST' and self.request.path.endswith('recover_password/'):
            return [AllowAny()]
        if self.request.method == 'POST' and self.request.path.endswith('update_password/'):
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        return super(UserViewset, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['password'] = make_password(data['password'])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    def destroy(self, request, *args, **kwargs):
        return super(UserViewset, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(UserViewset, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(UserViewset, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(UserViewset, self).partial_update(request, *args, **kwargs)

    @action(detail=True, methods=['put'])
    def update_password(self, request, pk=None):
        user = User.objects.get(id=pk)
        password = request.data.get('password')

        if password:
            hashed_password = make_password(password)
            user.password = hashed_password
            user.save()

            # Invalidate existing tokens by deleting them
            Token.objects.filter(user=user).delete()

            # Generate a new token for the user
            new_token, _ = Token.objects.get_or_create(user=user)

            return Response({"message": "Password updated successfully.", "token": new_token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "New password not provided."}, status=status.HTTP_400_BAD_REQUEST)


class CustomJWTAuthView(GenericAPIView):
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'user_individual'
    serializer_class = CustomJWTAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )
