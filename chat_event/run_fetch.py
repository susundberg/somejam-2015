import requests
import bs4
import re
import json

import datetime
import dateutil.parser

from django.conf import settings

LOGIN_URL    = settings.NUSUVEFO_BASE + "/kirjaudu"
CALENDER_JSON_URL = settings.NUSUVEFO_BASE + "/nusuvefo-kalenteri/events?format=raw&limit=0&ids=%(calid)s&date-start=%(from)s&date-end=%(until)s&my=0"
CALENDER_PATTERN = r"/nusuvefo-kalenteri\?task=ical\.download\&id=(\d+)"
TARGET_URL   = settings.NUSUVEFO_BASE + "/nusuvefo-kalenteri"

class FetchError(Exception):
  pass

class Provider:
  EPOC = datetime.datetime(1970, 1, 1)
  
  def __init__(self):
    self.session = requests.Session()
    pass
  
  def get_and_parse( self, url ):
    return bs4.BeautifulSoup( self.get_and_check( url ) )
  
  def get_and_check( self, url ):
    resp = self.session.get(url)
    if resp.status_code != 200:
      raise FetchError("Fetch to '%s' returned != 200: %s" % url, resp.content )
    return resp.content
    
                    
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
    
    target_url = settings.NUSUVEFO_BASE + login_url
    resp = self.session.post( target_url , payload  )
    if resp.status_code != 200:
      raise FetchError("Post to '%s' failed! : %s " % (target_url, resp.content) )
    soup = bs4.BeautifulSoup( resp.content )
    
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
  
  def _dt_to_timestamp( self, dt ):
    """ Convert datetime to timestamp, in python 3.3 we have timestamp() call for this .. """
    return ( dt - self.EPOC).total_seconds()
  
  def get_calender_events( self, calid,  dt_from=None , dt_until=None ):
      """ Get list of calendar events until given timespot.
          Returns:
            [ ( title, start, stop ), ... ]
      """
      if dt_from == None:
        dt_from = datetime.datetime.now() - datetime.timedelta( days = 1  )
      
      if dt_until == None:
        dt_until = datetime.datetime.now() + datetime.timedelta( days = 2 )
        
      target = CALENDER_JSON_URL % { 'calid' : calid, 
                                     'from'  : self._dt_to_timestamp( dt_from ), 
                                     'until' : self._dt_to_timestamp( dt_until )}
      
      json_str = self.get_and_check( target ) 
      
      try: 
        json_list = json.loads( json_str )
      except ValueError as error:
         raise FetchError("JSON conversion on get to '%s' failed %s with content: %s" % (target, error, json_str ))
      
      retlist = []
      
      
      for event in json_list:
        try:
          title = event["title"]
          start = dateutil.parser.parse( event["start"] )
          end   = dateutil.parser.parse( event["end"] )
        except KeyError as error:
          raise FetchError("Json object is missing field: %s. Content: %s " % (error, event) )
        except ValueError as error:
          raise FetchError("Json object contains invalid time-string : %s. Content: %s " % (error,event) )
        retlist.append( (title, start, end) )
      return retlist
    
        
    




