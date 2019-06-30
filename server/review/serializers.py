from django.contrib.auth import get_user_model
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from .models import Review

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    poster_name = serializers.ReadOnlyField(source='poster.full_name')
    poster_college = serializers.ReadOnlyField(source='poster.college.name')
    poster_picture = serializers.SerializerMethodField('get_avatar_thumbnail')

    class Meta:
        model = Review

    def __init__(self, *args, depth=1, **kwargs):
        super(ReviewSerializer, self).__init__(*args, **kwargs)

    def get_avatar_thumbnail(self, obj):
        if obj.poster.picture:
            return get_thumbnail(obj.poster.picture.path, '100x100', crop='center').url
        else:
            return None
