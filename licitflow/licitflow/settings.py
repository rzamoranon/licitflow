from pathlib import Path
import os
import dj_database_url
from urllib.parse import urlparse, quote_plus
from dotenv import load_dotenv  # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()  # Carga variables desde .env si existe

def env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}

def env_list(name, default=""):
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]

SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-me")
DEBUG = env_bool("DEBUG", True)

# Hosts / CSRF
# SUGERENCIA: evita '*' por defecto y confía en RAILWAY_PUBLIC_*.
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", "https://*.up.railway.app")

# Añadir dominio público de Railway si viene por env
railway_public = os.getenv("RAILWAY_PUBLIC_DOMAIN") or os.getenv("RAILWAY_PUBLIC_URL")
if railway_public:
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

APPEND_SLASH = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceros
    "widget_tweaks",

    # Apps locales
    "pages",
    "busqueda",
    "oportunidades",
    "documentos",
    "notificaciones",
    "crm",
    "core",
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
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "licitflow.wsgi.application"

#
# DB URL: prioridad a DATABASE_URL; si no existe y hay variables MYSQL_*, se arma automáticamente; si no, SQLite.
_db_url = os.getenv("DATABASE_URL")
if not _db_url:
    mysql_host = os.getenv("MYSQL_HOST")
    if mysql_host:
        mysql_user = os.getenv("MYSQL_USER", "root")
        mysql_password = os.getenv("MYSQL_PASSWORD", "")
        mysql_port = os.getenv("MYSQL_PORT", "3306")
        mysql_db = os.getenv("MYSQL_DATABASE", "railway")
        _db_url = (
            f"mysql://{quote_plus(mysql_user)}:{quote_plus(mysql_password)}"
            f"@{mysql_host}:{mysql_port}/{mysql_db}"
        )
    else:
        _db_url = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"

_ssl_required = _db_url.startswith(("postgres://", "postgresql://"))

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
_static_dir = BASE_DIR / "static"
STATICFILES_DIRS = [_static_dir] if _static_dir.exists() else []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Proxy/seguridad
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = "Lax"  # explícito
SECURE_CONTENT_TYPE_NOSNIFF = True
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    # HSTS opcional si tu dominio ya está siempre bajo HTTPS
    # SECURE_HSTS_SECONDS = 3600
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True

# Email (útil en dev; en prod cambia a tu SMTP)
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging: útil para ver errores en Railway
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
    },
}

# I18N
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Autenticación personalizada
AUTHENTICATION_BACKENDS = [
    "core.backends.EmailOrUsernameModelBackend",
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = "pages:login"
LOGIN_REDIRECT_URL = "pages:home"
LOGOUT_REDIRECT_URL = "pages:home"