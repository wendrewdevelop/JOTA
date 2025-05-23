import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User


@pytest.mark.django_db
class TestUserViewset:

    def setup_method(self):
        self.client = APIClient()

    def test_user_create(self):
        url = reverse('user-list')  # Confirme se está configurado como 'user-list' no router
        data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201
        assert User.objects.filter(email='test@example.com').exists()

    def test_user_list(self):
        User.objects.create_user(email='u1@test.com', password='123')
        User.objects.create_user(email='u2@test.com', password='123')

        url = reverse('user-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 2

    def test_update_password(self):
        user = User.objects.create_user(email='u3@test.com', password='123')
        url = reverse('user-update-password', kwargs={'pk': user.id})
        data = {"password": "newpassword123"}

        response = self.client.put(url, data, format='json')
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.check_password('newpassword123')
