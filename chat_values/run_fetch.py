
import requests
import bs4

class FetchError(Exception):
  pass

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'nettiapuanyt.settings'

from django.conf import settings

#except ImportError:
  #from nettiapuanyt import settings_secret 

  #class Settings:
    #pass
  #settings = Settings()
  #settings.SECRET_KEY = 'YtJFtu1fiufaa1cEqDdjxJUQ8PhQJI7zAdA77uz9x5narF4gLX'
  #settings.NUSUVEFO_USERNAME = "supauli"
  #settings.NUSUVEFO_PASSWORD = "578NF96oB6bv52PS"
  #settings.NUSUVEFO_BASE = "http://www.verke.org"


LOGIN_URL = settings.NUSUVEFO_BASE + "/kirjaudu"
CALENDER_URL= settings.NUSUVEFO_BASE + "/nusuvefo-kalenteri?task=ical.download&id=%d"



class Nusu:
  
  def __init__(self):
    self.session = requests.Session()
    pass
  
  def get_and_parse( self, url, resp=None ):
    if resp == None:
       resp = self.session.get(url)
    if resp.status_code != 200:
      raise FetchError("Fetch to '%s' returned != 200" % url )
    return bs4.BeautifulSoup(resp.content)
    
  def login(self):
    soup = self.get_and_parse(LOGIN_URL)
    
    forms = soup.findAll("form")
    if len(forms) != 1:
      raise FetchError("Reponse has more than one form")

    try:
      login_url    = forms[0]["action"]
      login_method = forms[0]["method"]
    except KeyError:
      raise FetchError("Form does not contain action or method")
    
    if login_method.upper() != "POST":
      raise FetchError("Method is not POST")

    hidden_inputs = forms[0].findAll("input", {'type':'hidden'})

    payload = { 'username' : settings.NUSUVEFO_USERNAME, 'password' : settings.NUSUVEFO_PASSWORD }
    for hidden in hidden_inputs:
      payload[ hidden["name"]] = hidden["value"]
      
    resp = self.session.post( settings.NUSUVEFO_BASE + login_url, payload )
    soup = self.get_and_parse( None, resp=resp )
    sys = soup.findAll("div", {'id':'system'})
    
    if len(sys)!=1:
      raise FetchError("Login failed probably: %s " % resp.content )
    

  def get_calendenders(self):
    soup = self.get_and_parse(TARGET_URL)
    containers = soup.findAll('dl', { 'id' : "dpcalendar_view_list"})
    if len(containers) != 1:
      raise FetchError("Invalid number of containers: %d " % len(containers) )
    container = containers[0]
    entries = []
    for entry in container.findAll("dt"):
      name = entry.font.string.strip()
      url = entry.a["href"]
      entries.append( ( name, url ))
    self.entries = entries
       
  def get_ical( self, calender_id ):
    resp = self.session.get( CALENDER_URL % calender_id )
    if resp.status_code != 200:
      raise FetchError("Fetch to '%s' returned != 200" % url )
    return resp.content
    




