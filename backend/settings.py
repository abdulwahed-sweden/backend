from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ======================
# Security Settings
# ======================
SECRET_KEY = 'django-insecure-yno21)%me%vq947%-r_g$l@_4!&jjknm2vwd1(c*#x*4p$^+6%'
DEBUG = True
ALLOWED_HOSTS = []


# ======================
# Application Definition
# ======================
INSTALLED_APPS = [
    # Django Core Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'rest_framework',
    'rest_framework_simplejwt',
    'django_otp',
    'django_otp.plugins.otp_totp',  # For TOTP (Time-Based OTP)

    # Local Apps
    'users',
    'pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # OTP Middleware
    'django_otp.middleware.OTPMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# ======================
# Database
# ======================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ======================
# Authentication & Authorization
# ======================
AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'users.validators.SwedishPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


# ======================
# Media & Static Files
# ======================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Directory where collected static files will be stored
STATIC_ROOT = BASE_DIR / 'staticfiles'  # or any other directory name

# Additional directories for static files
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Your app-specific static files
]


# ======================
# Internationalization
# ======================
LANGUAGE_CODE = 'sv'  # Swedish
TIME_ZONE = 'Europe/Stockholm'  # Swedish timezone
USE_I18N = True
USE_TZ = True


# ======================
# Default Primary Key
# ======================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ======================
# Additional Settings
# ======================
# Add any additional settings here, such as email configurations, logging, etc.