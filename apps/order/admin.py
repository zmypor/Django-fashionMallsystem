from django.contrib import admin
from django.utils.safestring import mark_safe
# Register your models here.
from .models import fashionMallOrder, fashionMallOrderProduct


@admin.register(fashionMallOrder)
class fashionMallOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'user','products', 'pay_method', 'pay_status', 
        'total_amount', 'paid_amount', 'pay_date', 'freight', 'add_date'
    )
    readonly_fields = (
        'order_number', 'user', 'pay_method', 'pay_status', 
        'total_amount', 'pay_date', 'freight'
    )
    list_display_links = ('order_number',)
    list_editable = ('pay_status',)
    list_filter = ('pay_method', 'pay_status', 'shipping_method')
    search_fields = ('order_number', 'user__username')


    @admin.display(description='订单商品')
    def products(self, obj):
        return mark_safe('</br>'.join([
            good.__str__() 
            for good in obj.fashionMallorderproduct_set.all()
        ]))
