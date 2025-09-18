import os
from pathlib import Path
import dj_database_url

# BASE_DIR = /home/projetos/WIS
# (settings.py está em src/config/settings.py → 3 "parent" até a raiz do projeto)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --- Básico / ambiente ---
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "insecure")
DEBUG = bool(int(os.getenv("DJANGO_DEBUG", "1")))
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Opcional: origens confiáveis para CSRF quando usar domínios reais/HTTPS
# Ex.: CSRF_TRUSTED_ORIGINS='https://example.com,https://sub.example.com'
_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [o for o in (s.strip() for s in _csrf.split(",")) if o]  # lista limpa

# --- Apps instalados ---
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceiros
    "rest_framework",

    # Seus apps
    "core",
    "people",
    "warrants",
    "dashboard",
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- URLs / WSGI ---
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
# (Se for usar ASGI/Channels, adicione: ASGI_APPLICATION = "config.asgi.application")

# --- Templates (corrige admin.E403) ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Com BASE_DIR na raiz, isso aponta para /home/projetos/WIS/templates
        # (e APP_DIRS=True já busca templates dentro de cada app)
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- Banco de dados ---
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # /home/projetos/WIS/db.sqlite3
        }
    }

# --- i18n / timezone ---
LANGUAGE_CODE = "pt-br"
# João Pessoa/PB → America/Recife (sem DST). Se preferir, use "America/Sao_Paulo".
TIME_ZONE = "America/Recife"
USE_I18N = True
USE_TZ = True

# --- Arquivos estáticos ---
# Com BASE_DIR na raiz do projeto:
#   collectstatic → /home/projetos/WIS/staticfiles
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Se tiver assets locais em desenvolvimento, você pode adicionar:
# STATICFILES_DIRS = [BASE_DIR / "static"]


# --- Arquivos de mídia (opcional) ---
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Outras configs ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
