from .serializers import CountrySerializer
from .models import Country
from rest_framework import viewsets


# Create your views here.
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
