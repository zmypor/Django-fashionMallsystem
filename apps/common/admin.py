from django.contrib import admin

# Register your models here.
from .models import fashionMallImagesAD

admin.site.site_title = "fashionMall"
admin.site.site_header = "fashionMall"
admin.site.index_title = "后台管理"

@admin.register(fashionMallImagesAD)
class fashionMallImagesADAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'image', 'url', 
        'slug', 'sort', 'add_date'
    )
    readonly_fields = ('image',)
    list_display_links = ('id', 'name')
    list_editable = ('sort',)
    list_filter = ('slug',)
    search_fields = ('name','slug')