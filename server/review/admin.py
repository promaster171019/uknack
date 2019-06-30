from django.contrib import admin

from review import models


@admin.register(models.Review)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'knack', 'item', 'poster', 'feedback', 'rating', 'created_at')
