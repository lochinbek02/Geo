from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from osgeo import gdal, ogr
from pathlib import Path
from .models import Location
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

def location_list(request):
    locations = Location.objects.all()
    return HttpResponse('<br>'.join([str(loc) for loc in locations]))

def read_raster(request):
    # Convert MEDIA_ROOT to Path and join with raster file name
    raster_file_path = Path(settings.MEDIA_ROOT) / 'shapefile.shp'
    
    # Open the raster file
    dataset = gdal.Open(str(raster_file_path))
    
    if dataset:
        band = dataset.GetRasterBand(1)
        array = band.ReadAsArray()
        
        return HttpResponse(array.tobytes(), content_type='application/octet-stream')
    else:
        return HttpResponse("Failed to open raster file", status=500)

def read_shapefile(request):
    gdal.SetConfigOption("SHAPE_RESTORE_SHX", "YES")
    shapefile_path = '/app/data/shapefiles/shapefile1.shp'
    datasource = ogr.Open(shapefile_path)
    
    if datasource:
        layer = datasource.GetLayer()
        
        features = []
        for feature in layer:
            geom = feature.GetGeometryRef()
            features.append({
                'type': 'Feature',
                'geometry': json.loads(geom.ExportToJson()),
                'properties': feature.items()
            })
        
        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }
        # return JsonResponse(geojson)  
        # HTML shabloniga JSON ma'lumotlarini yuborish
        return render(request, 'shapefile.html', {'geojson_data': mark_safe(json.dumps(geojson, cls=DjangoJSONEncoder))})
    else:
        return HttpResponse("Failed to open shapefile", status=500)