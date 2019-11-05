# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from socialapi import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialapi.settings')

app = Celery('socialapi')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto detect all task file in all Django installed app
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))