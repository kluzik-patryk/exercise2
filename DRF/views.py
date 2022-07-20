from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Country
from .serializers import CountrySerializer


# Create your views here.
class CountryAddApiView(APIView):

    def post(self, request, *args, **kwargs):
        data = {
            'country_name': request.data.get('country_name'),
            'spoken_language': request.data.get('spoken_language'),
            'population': request.data.get('population'),
        }

        serializer = CountrySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CountryViewApiView(APIView):

    def get_country(self, country_id):

        try:
            return Country.objects.get(id=country_id)
        except Country.DoesNotExist:
            return None

    def get(self, request, country_id, *args, **kwargs):
        country_instance = self.get_country(country_id=country_id)
        if not country_instance:
            return Response(
                {"res": "Object with country id does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CountrySerializer(country_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
