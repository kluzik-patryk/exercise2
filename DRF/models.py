from django.db import models


# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=50)
    spoken_language = models.TextField()
    population = models.IntegerField()

    def __str__(self):
        return self.country_name
