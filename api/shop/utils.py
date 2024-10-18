from django.db.models import Min, F, Sum

def spu_alias_annotate(queryset):
    """
    SPU 别名查询
    """
    return queryset.alias(
        price=Min("fashionMallsku__price"),
        dash_price=Min("fashionMallsku__dash_price"),
        stock=Sum("fashionMallsku__stock"),
        sale=Sum("fashionMallsku__sale"),
    ).annotate(
        price=F("price"),
        stock=F("stock"), 
        sale=F("sale"),
        dash_price=F("dash_price")
    ).order_by("-add_date")