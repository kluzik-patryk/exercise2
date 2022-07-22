from django.test import TestCase
from rest_framework.test import APIClient
from .models import Country
from .serializers import CountrySerializer


##### Functional tests  #####
class CountryTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.country_attribs = {
            "country_name": "Poland",
            "spoken_language": "Polish",
            "population": 38_000_000,
        }
        self.serializer_attribs = {
            "country_name": "France",
            "spoken_language": "French",
            "population": 67_390_000,
        }
        self.country = Country.objects.create(**self.country_attribs)
        self.serializer = CountrySerializer(instance=self.country)

    def test_incorrect_endpoint(self):
        response = self.client.get('/wrong_endpoint/', format="json")
        self.assertEqual(response.status_code, 404)

    def test_country_endpoint(self):
        response = self.client.get('/country/', format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["country_name"], "Poland")

    def test_post_country_correct_format(self):
        test_data = {
            "country_name": "England",
            "spoken_language": "English",
            "population": 55_980_000,
        }

        response = self.client.post('/country/', test_data)
        self.assertEqual(response.status_code, 201)

    def test_post_country_incorrect_format(self):
        test_data = {
            "country_name": "Sweden",
            "spoken_language": "Swedish",
            "population": "8000000f",
        }
        response = self.client.post('/country/', test_data)
        self.assertEqual(response.status_code, 400)

    def test_get_country_exists(self):
        response = self.client.get('/country/1/', format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["country_name"], "Poland")

    def test_get_country_does_not_exist(self):
        response = self.client.get('/country/2/', format="json")
        self.assertEqual(response.status_code, 404)
        self.assertRaises(KeyError, lambda: response.data["country_name"])

    #### UNIT TESTS ####

    def test_model_helper(self):
        self.assertEqual(self.country.__str__(), "Poland")

    def test_model_saving_and_retrieving_countries(self):
        saved_countries = Country.objects.all()
        self.assertEqual(saved_countries.count(), 1)

        Country.objects.create(country_name="Germany", spoken_language="German", population=80_000_000)

        # saved_countries = Country.objects.all()
        self.assertEqual(saved_countries.count(), 2)

        first_saved_country = saved_countries[0]
        second_saved_country = saved_countries[1]
        self.assertEqual(first_saved_country.country_name, 'Poland')
        self.assertEqual(second_saved_country.country_name, 'Germany')

    def test_model_wrong_data(self):
        self.assertRaises(ValueError,
                          lambda: Country.objects.create(
                              country_name="Japan",
                              spoken_language="Japanese",
                              population="a lot")
                          )

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['country_name', 'spoken_language', 'population'])

    def test_country_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["country_name"], self.country_attribs["country_name"])

    def test_population_field(self):
        self.serializer_attribs['population'] = 30_000_894.42

        serializer = CountrySerializer(data=self.serializer_attribs)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'population'})
