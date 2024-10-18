from django.contrib import admin
from django.utils.safestring import mark_safe
# Register your models here.
from .models import *


class fashionMallSPUImageInline(admin.TabularInline):
    '''Tabular Inline View for fashionMallSPUImage'''

    model = fashionMallSPUImage
    min_num = 1
    max_num = 8
    extra = 1


class fashionMallSKUInline(admin.TabularInline):
    '''Tabular Inline View for fashionMallSKU'''

    model = fashionMallSKU
    min_num = 1
    max_num = 20
    extra = 0
    verbose_name = "商品规格(SKU)"
    verbose_name_plural = "商品规格(SKU)"


class fashionMallSpecsValueInline(admin.TabularInline):
    '''Tabular Inline View for fashionMallSpecsValue'''

    model = fashionMallSpecsValue
    min_num = 3
    max_num = 20
    extra = 1
    

@admin.register(fashionMallSPU)
class fashionMallSPUAdmin(admin.ModelAdmin):
    '''Admin View for fashionMallSPU'''

    list_display = ('id', 'image', 'name', 'category', 'brand', 'is_sale', 'add_date')
    list_filter = ('category', 'brand', 'is_sale')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    search_help_text = "仅支持以商品名称搜索，模糊匹配"
    list_editable = ('is_sale',)
    inlines = [
        fashionMallSKUInline,
        fashionMallSPUImageInline,
    ]

    @admin.display(description='商品图')
    def image(self, obj):
        image = obj.fashionMallspuimage_set.first().image
        return mark_safe('<img src="%s" width="100" />' % image.url)
    

@admin.register(fashionMallSKUSpecs)
class fashionMallSKUSpecsAdmin(admin.ModelAdmin):
    '''Admin View for fashionMallSKUSpecs'''
    list_display = ('id', 'sku', 'specs', 'add_date')
    search_fields = ['sku__spu__name', ]
    search_help_text = "仅支持以商品名称搜索，模糊匹配"

    @admin.display(description='规格')
    def specs(self, obj):
        return [spec.__str__() for spec in obj.value.all()]


@admin.register(fashionMallSpecs)
class fashionMallSpecsAdmin(admin.ModelAdmin):
    '''Admin View for fashionMallSpecs'''

    list_display = ('id', 'name', 'add_date')
    list_display_links = ('id', 'name')
    inlines = [
        fashionMallSpecsValueInline,
    ]
    search_fields = ('name',)


@admin.register(fashionMallBrand)
class fashionMallBrandAdmin(admin.ModelAdmin):
    '''Admin View for fashionMallBrand'''

    list_display = ('id', 'name', 'add_date')


@admin.register(fashionMallCategory)
class fashionMallCategoryAdmin(admin.ModelAdmin):
    '''Admin View for fashionMallCategory'''

    list_display = ('id', 'name', 'parent', 'is_floor', 'sort', 'add_date')
    list_filter = ('parent',)
    list_editable = ('sort', 'is_floor')
