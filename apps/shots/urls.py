from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShotViewSet, SearchView

router = DefaultRouter()
router.register(r'shots', ShotViewSet, basename='shot')

urlpatterns = [
    path('search/', SearchView.as_view(), name='global_search'),
    path('', include(router.urls)),
]