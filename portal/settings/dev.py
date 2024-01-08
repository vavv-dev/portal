from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--in0a+6gu46lp+k)!l0&6%twz*g#o3jkel%lh5)!uwvm27@eoh"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


ID_NUMBER_ENCRYPTION_KEY = b"secureencryption"

PORT = 8000


try:
    from .local import *
except ImportError:
    pass
