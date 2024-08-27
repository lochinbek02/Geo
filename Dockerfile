# GDAL va boshqa kerakli kutubxonalar bilan bazaviy tasvirni tanlang
FROM python:3.11-slim

# Tizimda kerakli paketlarni o'rnatamiz
RUN apt-get update && \
    apt-get install -y \
        gdal-bin \
        libgdal-dev \
        build-essential \
        python3-dev \
        python3-gdal \
    && rm -rf /var/lib/apt/lists/*

# GDAL uchun muhit o'zgaruvchilarini sozlash
ENV GDAL_VERSION=3.9.2
ENV GDAL_DATA=/usr/share/gdal
ENV PROJ_LIB=/usr/share/proj

# Python kutubxonalarini o'rnatamiz
RUN pip install --no-cache-dir \
    numpy \
    wheel \
    setuptools \
    psycopg2-binary \
    django \
    djangorestframework \
    django-leaflet \
    geopandas \
    rasterio \
    pyproj

# Loyihani konteynerga nusxalash
WORKDIR /app
COPY . /app/

# Loyihani o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Django loyihasi portini ochamiz
EXPOSE 8000

# Django serverini ishga tushiramiz
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
