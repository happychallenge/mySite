from .common import *

DEBUG = True
ALLOWED_HOST = ['localhost', '127.0.0.1']
INSTALLED_APPS = [ 'debug_toolbar', ] + INSTALLED_APPS
MIDDLEWARE = [ 'debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE

STATIC_URL = '/static/'
STATICFILES_DIRS = (join(BASE_DIR, 'static'),)
STATIC_ROOT = join(BASE_DIR,  'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR,  'media')

# INTERNAL_IPS = ('127.0.0.1',)


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.naver.com'
EMAIL_HOST_USER = 'njyoon@naver.com'
EMAIL_HOST_PASSWORD = 'Wjdgml00$$'
EMAIL_PORT = 587