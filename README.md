# sqlHomeWork
Once upon a time, We'll work under the "store" directory

in setting.py:

change your correct USER/PASSWORD/HOST/PORT.
the default one follows exactly what assignment 2 does.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'xe',
        'USER': 'unist',
        'PASSWORD': 'unist',
        'HOST': '127.0.0.1', 
        'PORT': '1521',
    }
}


python manage.py startapp ${appname}
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     # Add our new application
    '${appname}.apps.${appname}Config',
]