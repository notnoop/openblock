"""
All deployment-specific config should be put in a module named
'real_settings.py'

This file should rarely need editing; if it does, you might want to
move the setting in question into real_settings.py

Known required settings are: %r
"""

import os
import imp

OBDEMO_DIR = os.path.normpath(os.path.dirname(__file__))
EBPUB_DIR = imp.find_module('ebpub')[1]
DJANGO_DIR = imp.find_module('django')[1]


########################
# CORE DJANGO SETTINGS #
########################

_required_settings=[
    'DEBUG',
]

TEMPLATE_DIRS = (
    os.path.join(OBDEMO_DIR, 'templates'),
    os.path.join(EBPUB_DIR, 'templates'),
    os.path.join(DJANGO_DIR, 'contrib', 'gis', 'templates'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.Loader'
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'ebpub.accounts.context_processors.user',
    'django.contrib.auth.context_processors.auth',
    'obdemo.context_processors.urls',
    #'django.core.context_processors.debug',
)

AUTHENTICATION_BACKENDS = (
    'ebpub.accounts.models.AuthBackend',
)

INSTALLED_APPS = (
    'obadmin.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'ebdata.blobs',
    'ebdata.geotagger',
    'ebpub.accounts',
    'ebpub.alerts',
    'ebpub.db',
    'ebpub.geocoder',
    'ebpub.petitions',
    'ebpub.preferences',
    'ebpub.savedplaces',
    'ebpub.streets',
    'django.contrib.humanize',
    'django.contrib.sessions',
    # Only need these 2 for some admin tasks, eg. configuration for
    # some scraper-related stuff for the everyblock package.  But I
    # haven't tried to figure out yet which scrapers this might be
    # useful for.
#    'everyblock.admin',
#    'everyblock.staticmedia',
)

APPS_FOR_TESTING = (
    # Don't need these installed at runtime, but I've put them here so
    # manage.py test can automatically find their tests.
    'ebdata.nlp',
    'ebdata.templatemaker',
    'ebdata.textmining',
    'ebpub.metros',
    'ebpub.utils',
)

INSTALLED_APPS = INSTALLED_APPS + APPS_FOR_TESTING

TEST_RUNNER = 'obadmin.testrunner.TestSuiteRunner'
#TEST_RUNNER='django.contrib.gis.tests.run_tests'

ROOT_URLCONF = 'obdemo.urls'
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'ebpub.accounts.middleware.UserMiddleware',
)

##################################
# CUSTOM EBPUB & OBDEMO SETTINGS #
##################################


POSTGIS_TEMPLATE = 'template_postgis'

# We've moved many settings to another (not-version-controlled) file.
# You'll get alerted by an error if anything required is not in that file.
# We import those settings twice: once up here to allow other settings
# to derive from them, and once at the end to override any defaults.

from real_settings import *

# The domain for your site.
_required_settings.append('EB_DOMAIN')

# This is the short name for your city, e.g. "chicago".
_required_settings.append('SHORT_NAME')

# Set both of these to distinct, secret strings that include two instances
# of '%s' each. Example: 'j8#%s%s' -- but don't use that, because it's not
# secret.
_required_settings.extend(['PASSWORD_CREATE_SALT', 'PASSWORD_RESET_SALT'])

# Database configuration as per
# http://docs.djangoproject.com/en/1.2/topics/db/multi-db/
_required_settings.append('DATABASES')

# The list of all metros this installation covers. This is a tuple of
# dictionaries, as per ebpub.settings.
_required_settings.append('METRO_LIST')

# Where to center citywide maps by default.
_required_settings.append('DEFAULT_MAP_CENTER_LON')
_required_settings.append('DEFAULT_MAP_CENTER_LAT')
_required_settings.append('DEFAULT_MAP_ZOOM')

EB_MEDIA_ROOT = OBDEMO_DIR + '/media' # necessary for static media versioning
EB_MEDIA_URL = '' # leave at '' for development
_required_settings.extend(['EB_MEDIA_URL', 'EB_MEDIA_ROOT'])

# Overrides datetime.datetime.today(), for development.
EB_TODAY_OVERRIDE = None

# Filesystem location of shapefiles for maps, e.g., '/home/shapefiles'.
# Used only by ebgeo/maps/tess.py
SHAPEFILE_ROOT = ''
_required_settings.append('SHAPEFILE_ROOT')

# For the 'autoversion' template tag.
_required_settings.append('AUTOVERSION_STATIC_MEDIA')
AUTOVERSION_STATIC_MEDIA = False


# Connection info for mapserver.
# Leave these alone if you're not using one;
# by default obdemo doesn't need it.
MAPS_POSTGIS_HOST = '127.0.0.1'
MAPS_POSTGIS_USER = ''
MAPS_POSTGIS_PASS = ''
MAPS_POSTGIS_DB = ''

_required_settings.extend([
        'MAPS_POSTGIS_HOST', 'MAPS_POSTGIS_USER', 'MAPS_POSTGIS_PASS',
        'MAPS_POSTGIS_DB',
])


# This is used as a "From:" in e-mails sent to users.
_required_settings.append('GENERIC_EMAIL_SENDER')

# Map stuff.
_required_settings.extend(['MAP_SCALES', 'SPATIAL_REF_SYS', 'MAP_UNITS'])
MAP_SCALES = [614400, 307200, 153600, 76800, 38400, 19200, 9600, 4800, 2400, 1200]
SPATIAL_REF_SYS = '900913' # Spherical Mercator
MAP_UNITS = 'm' # see ebpub.utils.mapmath for allowed unit types

# Filesystem location of tilecache config (e.g., '/etc/tilecache/tilecache.cfg').
# obdemo doesn't use a tilecache out of the box.
TILECACHE_CONFIG = '/etc/tilecache.cfg'
TILECACHE_ZOOM = 17
TILECACHE_LAYER = 'osm'
TILECACHE_VERSION = '1.0.0'
TILECACHE_EXTENSION = 'png'

# Filesystem location of scraper log.
_required_settings.append('SCRAPER_LOGFILE_NAME')

# XXX Unused?
#DATA_HARVESTER_CONFIG = {}

# XXX Unused?
#MAIL_STORAGE_PATH = '/home/mail'

# If this cookie is set with the given value, then the site will give the user
# staff privileges (including the ability to view non-public schemas).
_required_settings.extend(['STAFF_COOKIE_NAME', 'STAFF_COOKIE_VALUE'])

# TODO: instead of bundling a rather bulky openlayers, our installer
# should maybe download and build both an optimized profile,
# and an un-minified version, and toggle them here based on DEBUG.
OPENLAYERS_URL = '/scripts/openlayers-2.9.1/OpenLayers.js'

# Re-import from real_settings to override any defaults in this file.
from real_settings import *

for name in _required_settings:
    if not name in globals():
        raise NameError("Required setting %r was not defined in real_settings.py or settings.py" % name)


# Logging setup. There's a bit of hackery to make sure we don't set up
# handlers more than once; see
# http://stackoverflow.com/questions/342434/python-logging-in-django
import logging, threading
_lock = threading.Lock()
with _lock:
    if getattr(logging, '_is_set_up', None) is None:
        logging._is_set_up = True
        if not logging.getLogger().handlers:
            # TODO: configurable file handlers, level...
            logging.basicConfig(level=logging.INFO,
                                format="%(asctime)-15s %(levelname)-8s %(message)s")

__doc__ = __doc__ % _required_settings
