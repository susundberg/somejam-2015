import requests
import bs4
import re

from django.conf import settings

LOGIN_URL    = settings.NUSUVEFO_BASE + "/kirjaudu"
CALENDER_URL = settings.NUSUVEFO_BASE + "/nusuvefo-kalenteri?task=ical.download&id=%s"
CALENDER_PATTERN = r"/nusuvefo-kalenteri\?task=ical\.download\&id=(\d+)"
TARGET_URL   = settings.NUSUVEFO_BASE + "/nusuvefo-kalenteri"

class FetchError(Exception):
  pass

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
    url_pattern = re.compile( CALENDER_PATTERN, re.I )
    
    for entry in container.findAll("dt"):
      name = entry.font.string.strip()
      url = entry.a["href"]
      url_match = url_pattern.match( url )
      if url_match:
         entries.append( ( name, url_match.group(1) ) )
      else:
         print "Warning: did not match:" + url
    return entries
       
  def get_ical( self, calender_id ):
    resp = self.session.get( CALENDER_URL % calender_id )
    if resp.status_code != 200:
      raise FetchError("Fetch to '%s' returned != 200" % url )
    return resp.content
    




