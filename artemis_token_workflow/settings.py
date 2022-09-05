"""
Django settings for artemis_token_workflow project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from django.utils.text import format_lazy

from django.urls import reverse_lazy
from .config_loader import ConfigLoader
import os
import saml2
import saml2.saml
import shutil

######################################
# HELPERS
######################################

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

if os.environ.get("DJANGO_CONFIG", "").lower() == "dev":
    config_file = "dev"
else:
    config_file = "prod"

config = ConfigLoader(
    [BASE_DIR / "config" / f"{config_file}.json", BASE_DIR / "config" / "base.json"]
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = config["django.secret-key"]
DEBUG = config["django.debug"]

######################################
# External / Proxy
######################################

ALLOWED_HOSTS = []

######################################
# Applications / Plugins
######################################

INSTALLED_APPS = [
    "app.apps.AppConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djangosaml2",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangosaml2.middleware.SamlSessionMiddleware",
]

ROOT_URLCONF = "artemis_token_workflow.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "artemis_token_workflow.wsgi.application"


######################################
# Database
######################################
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "data" / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

######################################
# Internationalization
######################################
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "de-de"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

######################################
# AUTHENTICATION
######################################
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "djangosaml2.backends.Saml2Backend",
)

# Django setting to which URL an unauthenticated user is forwarded.
# Default: Uses the SAML login view.
LOGIN_URL = format_lazy(
    "{saml2_prefix}/login", saml2_prefix=reverse_lazy("saml2_prefix")
)


######################################
# Djangosaml2
######################################
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# The application must provide the endpoints as part of the metadata to the IdP
# However, Django does not know its external URL thus we need to manually provide it
# Supply an URL with a trailing slash. Example: https://my.app.com/
SAML_EXTERNAL_HOST = "http://localhost:8000/"
# The path prefix under which the djangosaml.urls are `included`.
# Supply an URL with a trailing slash.
SAML_PATH_PREFIX = "v1/login/saml2/"
SAML_EXTERNAL_URL = SAML_EXTERNAL_HOST + SAML_PATH_PREFIX
# Create a Django user if the SAML2 user does not exist.
SAML_CREATE_UNKNOWN_USER = True

######################################
# Djangosaml2 / PySAML2
######################################
# These are the config options for PySAML2 which is used under the hood by Djangosaml2
# A lot of config options CANNOT be customized because they are hardcoded into Djangosaml2.
SAML_CONFIG = {
    # full path to the xmlsec1 binary programm
    "xmlsec_binary": shutil.which("xmlsec1"),
    # your entity id, usually your subdomain plus the url to the metadata view
    "entityid": SAML_EXTERNAL_URL + "metadata/",
    # directory with attribute mapping
    "attribute_map_dir": os.path.join(BASE_DIR, "config/attributemaps"),
    # Permits to have attributes not configured in attribute-mappings
    # otherwise...without OID will be rejected
    "allow_unknown_attributes": True,
    # this block states what services we provide
    "service": {
        # we are just a lonely SP
        "sp": {
            "name": "Federated Django sample SP",
            "name_id_format": saml2.saml.NAMEID_FORMAT_TRANSIENT,
            # For Okta add signed logout requests. Enable this:
            # "logout_requests_signed": True,
            "endpoints": {
                # url and binding to the assetion consumer service view
                # do not change the binding or service name
                "assertion_consumer_service": [
                    (SAML_EXTERNAL_URL + "acs/", saml2.BINDING_HTTP_POST),
                ],
                # url and binding to the single logout service view
                # do not change the binding or service name
                "single_logout_service": [
                    # Disable next two lines for HTTP_REDIRECT for IDP's that only support HTTP_POST. Ex. Okta:
                    (SAML_EXTERNAL_URL + "ls/", saml2.BINDING_HTTP_REDIRECT),
                    (SAML_EXTERNAL_URL + "ls/post", saml2.BINDING_HTTP_POST),
                ],
            },
            #         "signing_algorithm": saml2.xmldsig.SIG_RSA_SHA256,
            #         "digest_algorithm": saml2.xmldsig.DIGEST_SHA256,
            #         # Mandates that the identity provider MUST authenticate the
            #         # presenter directly rather than rely on a previous security context.
            #         "force_authn": False,
            #         # Enable AllowCreate in NameIDPolicy.
            #         "name_id_format_allow_create": False,
            #         # attributes that this project need to identify a user
            #         "required_attributes": ["givenName", "sn", "mail"],
            #         # attributes that may be useful to have but not required
            #         "optional_attributes": ["eduPersonAffiliation"],
            #         "want_response_signed": True,
            #         "authn_requests_signed": True,
            #         "logout_requests_signed": True,
            #         # Indicates that Authentication Responses to this SP must
            #         # be signed. If set to True, the SP will not consume
            #         # any SAML Responses that are not signed.
            #         "want_assertions_signed": True,
            #         "only_use_keys_in_metadata": True,
            #         # When set to true, the SP will consume unsolicited SAML
            #         # Responses, i.e. SAML Responses for which it has not sent
            #         # a respective SAML Authentication Request.
            #         "allow_unsolicited": False,
            #         # in this section the list of IdPs we talk to are defined
            #         # This is not mandatory! All the IdP available in the metadata will be considered instead.
            #         "idp": {
            #             # we do not need a WAYF service since there is
            #             # only an IdP defined here. This IdP should be
            #             # present in our metadata
            #             # the keys of this dictionary are entity ids
            #             "https://localhost/simplesaml/saml2/idp/metadata.php": {
            #                 "single_sign_on_service": {
            #                     saml2.BINDING_HTTP_REDIRECT: "https://localhost/simplesaml/saml2/idp/SSOService.php",
            #                 },
            #                 "single_logout_service": {
            #                     saml2.BINDING_HTTP_REDIRECT: "https://localhost/simplesaml/saml2/idp/SingleLogoutService.php",
            #                 },
            #             },
            #         },
        },
    },
    # # where the remote metadata is stored, local, remote or mdq server.
    # # One metadatastore or many ...
    "metadata": {
        # "local": [path.join(BASEDIR, "remote_metadata.xml")],
        "remote": [
            {"url": "https://samltest.id/saml/idp"},
        ],
        # "mdq": [
        #     {
        #         "url": "https://ds.testunical.it",
        #         "cert": "certficates/others/ds.testunical.it.cert",
        #     }
        # ],
    },
    # # set to 1 to output debugging information
    # "debug": 1,
    # # Signing
    # "key_file": path.join(BASEDIR, "private.key"),  # private part
    # "cert_file": path.join(BASEDIR, "public.pem"),  # public part
    # # Encryption
    # "encryption_keypairs": [
    #     {
    #         "key_file": path.join(BASEDIR, "private.key"),  # private part
    #         "cert_file": path.join(BASEDIR, "public.pem"),  # public part
    #     }
    # ],
    # own metadata settings
    "contact_person": [
        {
            "given_name": "Dominik",
            "sur_name": "Fuchs",
            "company": "KIT - KASTEL",
            "email_address": "programmieren-vorlesung@kit.edu",
            "contact_type": "technical",
        },
    ],
    # # you can set multilanguage information here
    # "organization": {
    #     "name": [("Yaco Sistemas", "es"), ("Yaco Systems", "en")],
    #     "display_name": [("Yaco", "es"), ("Yaco", "en")],
    #     "url": [("http://www.yaco.es", "es"), ("http://www.yaco.com", "en")],
    # },
}

######################################
# ARTEMIS
######################################
ARTEMIS_SERVER_URL = config["artemis.server"]
ARTEMIS_USER = config["artemis.user"]
ARTEMIS_PASSWORD = config["artemis.password"]
