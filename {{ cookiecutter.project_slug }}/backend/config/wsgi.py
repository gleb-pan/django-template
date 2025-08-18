"""
WSGI config for seedproj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Грузим .env рядом с manage.py (или выше)
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "config.settings.prod"
)

application = get_wsgi_application()
