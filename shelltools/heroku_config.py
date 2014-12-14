#!/usr/bin/python

import nettiapuanyt.settings_secret as secret_settings
from subprocess import call


def heroku_config_set( key, value ):
  call( ( "heroku","config:set", "%s=%s" % (key,value) ) )

  
for varname in dir(secret_settings):
  if varname.startswith("_"):
    continue
  
  heroku_config_set( varname, getattr(secret_settings,varname) )






