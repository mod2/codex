# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'Put your secret key here. Keep it secret. Keep it safe.'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Remove the integrations you don't care about
INTEGRATIONS = {
    'dropbox': {
        'key': 'your dropbox key here',
    },
    'flickr': {
        'key': 'your flickr key here',
        'secret': 'your flickr secret here',
    },
}

DEFAULT_FROM_EMAIL = 'system@localhost'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
