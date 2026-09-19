from pathlib import Path
import os
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.getenv('DJANGO_SECRET_KEY','dev-only-change-me')
DEBUG=True
ALLOWED_HOSTS=['127.0.0.1','localhost']
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','accounts','shop','payments']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='secureshop.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='secureshop.wsgi.application'
DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS=[]
LANGUAGE_CODE='fr-fr'; TIME_ZONE='Africa/Kinshasa'; USE_I18N=True; USE_TZ=True
STATIC_URL='static/'; STATICFILES_DIRS=[BASE_DIR/'static']; MEDIA_URL='/media/'; MEDIA_ROOT=BASE_DIR/'media'; DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_REDIRECT_URL='/produits/'; LOGOUT_REDIRECT_URL='/'; LOGIN_URL='/accounts/login/'
SESSION_COOKIE_HTTPONLY=True; SESSION_COOKIE_SAMESITE='Lax'
# Activer en production HTTPS :
# SESSION_COOKIE_SECURE=True; CSRF_COOKIE_SECURE=True; SECURE_SSL_REDIRECT=True
PAYMENT_HMAC_KEY=os.getenv('PAYMENT_HMAC_KEY','tp-demo-hmac-key-change-me')
if os.environ.get("RENDER"):
    ALLOWED_HOSTS.append(os.environ.get("RENDER_EXTERNAL_HOSTNAME"))
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
if os.environ.get("RENDER"):
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True