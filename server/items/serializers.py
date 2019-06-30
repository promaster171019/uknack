from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from .models import Item, Category
from user_auth.serializers import KnackProfileSerializer

User = get_user_model()


class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    photos = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    def __init__(self, *args, depth=1, **kwargs):
        super(ItemSerializer, self).__init__(*args, **kwargs)
        if depth >= 0:
            self.fields['owner'] = KnackProfileSerializer(depth=depth, read_only=True)

    def get_created_at(self, obj):
        return obj.created_at.strftime('%m/%d/%y')

    def get_modified_at(self, obj):
        return obj.modified_at.strftime('%m/%d/%y')

    class Meta:
        model = Item
        read_only_fields = ('views',)

    def get_photos(self, obj):
        photos = []
        if obj.photo0:
            if settings.SITE_URL not in obj.photo0.url:
                photos.append(settings.SITE_URL + obj.photo0.url)
            else:
                photos.append(obj.photo0.url)
        if obj.photo1:
            if settings.SITE_URL not in obj.photo1.url:
                photos.append(settings.SITE_URL + obj.photo1.url)
            else:
                photos.append(obj.photo1.url)
        if obj.photo2:
            if settings.SITE_URL not in obj.photo2.url:
                photos.append(settings.SITE_URL + obj.photo2.url)
            else:
                photos.append(obj.photo2.url)
        if obj.photo3:
            if settings.SITE_URL not in obj.photo3.url:
                photos.append(settings.SITE_URL + obj.photo3.url)
            else:
                photos.append(obj.photo3.url)
        if obj.photo4:
            if settings.SITE_URL not in obj.photo4.url:
                photos.append(settings.SITE_URL + obj.photo4.url)
            else:
                photos.append(obj.photo4.url)
        return photos

    def get_thumbnails(self, obj):
        photos = []
        if obj.photo0:
            photos.append(obj.photo0.path)
        if obj.photo1:
            photos.append(obj.photo1.path)
        if obj.photo2:
            photos.append(obj.photo2.path)
        if obj.photo3:
            photos.append(obj.photo3.path)
        if obj.photo4:
            photos.append(obj.photo4.path)
        thumbs = []
        for photo in photos:
            thumbs.append(get_thumbnail(photo, '440x296', crop='center').url)
        return thumbs

    def get_rating(self, obj):
        average = 0.0
        if obj.item_reviews.count() > 0:
            for item in obj.item_reviews.all():
                average += item.rating
            average = average / obj.item_reviews.count()
        return average

    def get_rating_count(self, obj):
        return obj.item_reviews.count()


class ProfileItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    photos = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    def __init__(self, *args, depth=1, **kwargs):
        super(ProfileItemSerializer, self).__init__(*args, **kwargs)

    def get_created_at(self, obj):
        return obj.created_at.strftime('%m/%d/%y')

    def get_modified_at(self, obj):
        return obj.modified_at.strftime('%m/%d/%y')

    class Meta:
        model = Item
        read_only_fields = ('views',)
        exclude = ('owner', )

    def get_photos(self, obj):
        photos = []
        if obj.photo0:
            photos.append(obj.photo0.url)
        if obj.photo1:
            photos.append(obj.photo1.url)
        if obj.photo2:
            photos.append(obj.photo2.url)
        if obj.photo3:
            photos.append(obj.photo3.url)
        if obj.photo4:
            photos.append(obj.photo4.url)
        return photos

    def get_thumbnails(self, obj):
        photos = []
        if obj.photo0:
            photos.append(obj.photo0.path)
        if obj.photo1:
            photos.append(obj.photo1.path)
        if obj.photo2:
            photos.append(obj.photo2.path)
        if obj.photo3:
            photos.append(obj.photo3.path)
        if obj.photo4:
            photos.append(obj.photo4.path)
        thumbs = []
        for photo in photos:
            thumbs.append(get_thumbnail(photo, '440x296', crop='center').url)
        return thumbs

    def get_rating(self, obj):
        average = 0.0
        if obj.item_reviews.count() > 0:
            for item in obj.item_reviews.all():
                average += item.rating
            average = average / obj.item_reviews.count()
        return average

    def get_rating_count(self, obj):
        return obj.item_reviews.count()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
