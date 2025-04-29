from __future__ import absolute_import, unicode_literals
# это гарантирует, что при запуске Django также запускается Celery
from .celery import app as celery_app

__all__ = ('celery_app',)