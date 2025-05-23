from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from news.models import News


User = get_user_model()

class NewsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass'
        )
        self.news = News.objects.create(
            title='Test News',
            content='This is a test news content',
            published_at='2024-05-23T12:00:00Z'
        )
        self.list_url = reverse('news-list')
        self.detail_url = reverse('news-detail', kwargs={'pk': self.news.pk})

    def test_list_news(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_news(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_news(self):
        self.client.force_authenticate(user=self.user)
        file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'title': 'Another News',
            'content': 'Another news content',
            'published_at': '2024-05-24T12:00:00Z',
            'post_image': file
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_news(self):
        self.client.force_authenticate(user=self.user)
        file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'title': 'Another News',
            'content': 'Another news content',
            'published_at': '2024-05-24T12:00:00Z',
            'post_image': file
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_news(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Partially Updated News'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_news(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
