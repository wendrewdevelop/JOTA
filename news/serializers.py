from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'news_id',
            'title',
            'subtitle',
            'post_image',
            'content',
            'published_at',
            'author',
            'category',
            'plan',
            'status',
            'scheduled_post'
        ]
        read_only_fields = [
            'news_id',
            'published_at'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        return data

    def get_post_image_url(self, obj):
        request = self.context.get('request')
        if obj.post_image and request:
            return request.build_absolute_uri(obj.post_image.url)
        elif obj.post_image:
            return obj.post_image.url
        return None
