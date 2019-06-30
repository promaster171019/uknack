from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from .models import Knack, KnackIdea, Category
from user_auth.serializers import KnackProfileSerializer
from review.serializers import ReviewSerializer

User = get_user_model()


class KnackSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    photos = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    reviews = ReviewSerializer(source='knack_reviews', many=True)
    ready_to_repost = serializers.SerializerMethodField()
    repost_available_in = serializers.SerializerMethodField()

    class Meta:
        model = Knack
        exclude = ('deleted', 'video', 'reposted_at', 'owner')

    def __init__(self, *args, depth=1, **kwargs):
        super(KnackSerializer, self).__init__(*args, **kwargs)
        if depth >= 0:
            self.fields['owner'] = KnackProfileSerializer(depth=depth, read_only=True)

    def get_ready_to_repost(self, obj):
        return obj.ready_to_repost

    def get_repost_available_in(self, obj):
        return obj.repost_available_in

    def get_created_at(self, obj):
        return obj.created_at.strftime('%m/%d/%y')

    def get_modified_at(self, obj):
        return obj.modified_at.strftime('%m/%d/%y')

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
        if obj.knack_reviews.count() > 0:
            for item in obj.knack_reviews.all():
                average += item.rating
            average = average / obj.knack_reviews.count()
        return average

    def get_rating_count(self, obj):
        return obj.knack_reviews.count()

    def is_valid(self, raise_exception=False):
        # photo = self.initial_data.pop('photo')[0]
        # if not isinstance(photo, str):
        #     self.initial_data.update({'photo': photo})
        # video = self.initial_data.pop('video')[0]
        # if not isinstance(video, str):
        #     self.instance.video = video
        return super(KnackSerializer, self).is_valid(raise_exception)


class ProfileKnackSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    photos = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    reviews = ReviewSerializer(source='knack_reviews', many=True)
    ready_to_repost = serializers.SerializerMethodField()
    repost_available_in = serializers.SerializerMethodField()

    class Meta:
        model = Knack
        exclude = ('deleted', 'video', 'reposted_at', 'owner')

    def __init__(self, *args, depth=1, **kwargs):
        super(ProfileKnackSerializer, self).__init__(*args, **kwargs)

    def get_ready_to_repost(self, obj):
        return obj.ready_to_repost

    def get_repost_available_in(self, obj):
        return obj.repost_available_in

    def get_created_at(self, obj):
        return obj.created_at.strftime('%m/%d/%y')

    def get_modified_at(self, obj):
        return obj.modified_at.strftime('%m/%d/%y')

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
        if obj.knack_reviews.count() > 0:
            for item in obj.knack_reviews.all():
                average += item.rating
            average = average / obj.knack_reviews.count()
        return average

    def get_rating_count(self, obj):
        return obj.knack_reviews.count()


class KnackIdeaSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    photos = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    # how_charge = serializers.SerializerMethodField()

    def get_how_charge(self, obj):
        return 'FLAT' if obj.how_charge == 'Flat Fee' else 'HR'

    class Meta:
        model = KnackIdea

    def get_photos(self, obj):
        return [image.photo.url for image in obj.knackideaimage_set.all()]

    def get_thumbnails(self, obj):
        arr = []
        photos = obj.knackideaimage_set.all()
        for item in photos:
            url = get_thumbnail(item.photo, '219x147', crop='center').url
            arr.append(url)
        return arr


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
