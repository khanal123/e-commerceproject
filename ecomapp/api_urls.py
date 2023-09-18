from django.urls import path, include 
from rest_framework import routers
from .views import ItemViewSet , AdViewSet , ItemFilterListView

# create a variable 
router = routers.DefaultRouter()
router.register('item',ItemViewSet)
router.register('ad',AdViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('filter_item_api',ItemFilterListView.as_view(),name='filter_item_api')
]


