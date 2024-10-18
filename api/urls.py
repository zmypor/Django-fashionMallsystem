from django.urls import path, include

app_name = "fashionMall_api"

urlpatterns = [
    path('article/', include('api.article.urls')),
    path('auth/', include('api.auth.urls')),
    path('page/', include('api.flatpages.urls')),
    path('shop/', include('api.shop.urls')),
    path('cart/', include('api.cart.urls')),
    path('address/', include('api.address.urls')),
    path('cash/', include('api.cash.urls')),
    path('order/', include('api.order.urls')),
    path('common/', include('api.common.urls')),
    path('comment/', include('api.comment.urls')),
]


