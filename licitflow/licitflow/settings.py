from pathlib import Path
import os
import dj_database_url
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent

def env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}

def env_list(name, default=""):
    return [x for x in os.getenv(name, default).split(",") if x.strip()]

SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-me")
DEBUG = env_bool("DEBUG", False)

# Hosts / CSRF
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "*")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", "https://*.up.railway.app")

# Añadir dominio público de Railway si viene por env
railway_public = os.getenv("RAILWAY_PUBLIC_DOMAIN") or os.getenv("RAILWAY_PUBLIC_URL")
if railway_public:
    # Normaliza a host u origen
    if railway_public.startswith("http"):
        origin = railway_public.rstrip("/")
        host = urlparse(railway_public).hostname
    else:
        origin = f"https://{railway_public}"
        host = railway_public
    if host and host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)
    if origin and origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # estáticos en prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "licitflow.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "licitflow.wsgi.application"

# DB: usa DATABASE_URL si existe; activa SSL sólo si es Postgres
_db_url = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
_ssl_required = _db_url.startswith("postgres://") or _db_url.startswith("postgresql://")

_db_config = dj_database_url.parse(
    _db_url,
    conn_max_age=600,
    ssl_require=_ssl_required,
)

# Si es SQLite, elimina OPTIONS (p.ej. sslmode) que rompe la conexión
if _db_config.get("ENGINE", "").endswith("sqlite3"):
    _db_config.pop("OPTIONS", None)

DATABASES = {"default": _db_config}

# Static
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Solo añade STATICFILES_DIRS si la carpeta existe (evita errores en collectstatic)
_static_dir = BASE_DIR / "static"
STATICFILES_DIRS = [_static_dir] if _static_dir.exists() else []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# Opcional para mantener solo archivos versionados por hash
# WHITENOISE_KEEP_ONLY_HASHED_FILES = True

# Proxy/seguridad
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    # Puedes ajustar HSTS si quieres:
    # SECURE_HSTS_SECONDS = 3600
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True

# I18N
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"