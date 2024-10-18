from django.contrib import admin

# Register your models here.
from .models import fashionMallComment


@admin.register(fashionMallComment)
class fashionMallCommentAdmin(admin.ModelAdmin):
    '''Admin View for fashionMallComment'''

    list_display = ('id', 'user', 'content', 'object_id', 'content_type', 'score', 'status', 'add_date')
    readonly_fields = ('user', 'object_id', 'content_type')
