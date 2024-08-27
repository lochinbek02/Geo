from django.db import models
from django.contrib.gis.db import models as geomodels

class Location(geomodels.Model):
    name = models.CharField(max_length=100)
    point = geomodels.PointField()  # Geometrik nuqta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
