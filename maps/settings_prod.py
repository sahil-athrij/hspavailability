# DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'hospital',
        'USER': 'hospital',
        'PASSWORD': 'hospitals',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
