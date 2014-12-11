# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'Put your secret key here. Keep it secret. Keep it safe.'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
