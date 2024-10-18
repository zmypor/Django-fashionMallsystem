from django.contrib import admin

# Register your models here.
from .models import fashionMallAddress

# admin.site.register([fashionMallAddress, fashionMallUserAddress])

@admin.register(fashionMallAddress)
class fashionMallAddressAdmin(admin.ModelAdmin):
    '''Admin View for fashionMallAddress'''

    list_display = ('id', 'name', 'parent', 'add_date')
    list_display_links = ('id', 'name')