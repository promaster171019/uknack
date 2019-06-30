import six
from django.db import models
from django.conf import settings

from knacks.models import Knack
from items.models import Item

User = settings.AUTH_USER_MODEL


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


@six.python_2_unicode_compatible
class Review(models.Model):
    knack = models.ForeignKey(Knack, related_name='knack_reviews', blank=True, null=True)
    item = models.ForeignKey(Item, related_name='item_reviews', blank=True, null=True)

    owner = models.ForeignKey(User, related_name='items_owner', blank=True, null=True)
    poster = models.ForeignKey(User, related_name='reviews_poster', blank=True, null=True)

    feedback = models.TextField()
    rating = IntegerRangeField(min_value=1, max_value=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Review From %s' % self.poster.email
