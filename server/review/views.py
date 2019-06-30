from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Review
from knacks.models import Knack
from items.models import Item
from . import serializers


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    PAGINATE_BY_PARAM = 'page_size'

    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def check_object_permissions(self, request, obj):
        # Check if a user is the owner of the knack if a request is not safe
        if request.method not in SAFE_METHODS and request.user != obj.poster:
            self.permission_denied(request)

        return super(ReviewViewSet, self).check_object_permissions(request, obj)

    def perform_create(self, serializer):
        id = self.request.data['item_id']
        if self.request.data['item_type'] == 'knack':
            try:
                knack = Knack.objects.get(pk=id)
            except ObjectDoesNotExist:
                return Response({'details': 'Knack does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(poster=self.request.user, knack=knack, owner=knack.owner)
        elif self.request.data['item_type'] == 'item':
            try:
                item = Item.objects.get(pk=id)
            except ObjectDoesNotExist:
                return Response({'details': 'Item does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(poster=self.request.user, item=item, owner=item.owner)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # Override the method to count views
        instance = self.get_object()

        # This will hit db only once and will not trigger signals -> will not update modified_at field
        instance.__class__.objects.filter(pk=instance.pk).update(views=F('views') + 1)
        # Add one to instance views to display the correct value. Do not save the instance!
        instance.views += 1

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super(ReviewViewSet, self).get_queryset()
        queryset = queryset.order_by('-created_at')
        return queryset
