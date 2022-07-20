from django.urls import path, include
from .views import CountryViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', CountryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]