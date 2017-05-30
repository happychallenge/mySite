from .common import *

DEBUG = True
ALLOWED_HOST = []
INSTALLED_APPS = [ 'debug_toolbar', ] + INSTALLED_APPS
MIDDLEWARE = [ 'debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE

STATIC_URL = '/static/'
STATICFILES_DIRS = (join(BASE_DIR, 'mySite', 'static'),)
STATIC_ROOT = join(BASE_DIR, 'mySite', 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'mySite', 'media')

INTERNAL_IPS = ('127.0.0.1',)
