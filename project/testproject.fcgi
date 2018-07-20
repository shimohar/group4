#!/usr/bin/python
import sys, os
sys.path.insert(0, "/home/joelennon/python")
os.environ['DJANGO_SETTINGS_MODULE'] = "testproject.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
