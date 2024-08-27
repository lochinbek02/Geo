from django.urls import path
from .views import location_list,read_raster,read_shapefile

urlpatterns = [
    path('locations/', location_list, name='location_list'),
    path('read-raster/', read_raster, name='read_raster'),
    path('read-shapefile/', read_shapefile, name='read_shapefile'),
]
