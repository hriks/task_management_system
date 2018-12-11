"""
WSGI config for task_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
#
# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_management.settings")
#
# application = get_wsgi_application()

import os
from django.core.wsgi import get_wsgi_application
from core.settings import WEBSOCKET_URL
os.environ.update(DJANGO_SETTINGS_MODULE='task_management.settings')

if os.environ.get('PATH_INFO').startswith(WEBSOCKET_URL):
    print "as"
else:
    print "asasasas"
application = get_wsgi_application()
