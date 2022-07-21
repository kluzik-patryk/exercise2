from django.test import TestCase
from rest_framework.test import APIClient
from .models import Country


# Create your tests here.
class CountryTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.country = Country.objects.create(country_name="Poland", spoken_language="Polish", population=38_000_000)

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
