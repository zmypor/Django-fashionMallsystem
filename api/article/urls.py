from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(
    'category', 
    views.fashionMallArticleCategoryViewSet, 
    basename="category"
)
router.register(
    'content', 
    views.fashionMallArticleContentViewSet, 
    basename="content"
)


urlpatterns = router.urls