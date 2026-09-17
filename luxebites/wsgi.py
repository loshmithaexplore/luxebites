"""
WSGI config for luxebites project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

path = "/home/Loshmitha/luxe-bites"

if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luxebites.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()