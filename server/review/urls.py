from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
