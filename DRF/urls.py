from django.urls import path, include
from .views import CountryAddApiView, CountryViewApiView

urlpatterns = [
    path('', CountryAddApiView.as_view()),
    path('<int:country_id>/', CountryViewApiView.as_view()),
]