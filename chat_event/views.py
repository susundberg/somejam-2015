from django.views.generic.list import ListView
from django.http import HttpResponse

from chat_event.models import Event


import datetime
import pytz
import json


def get_now():
  return datetime.datetime.utcnow().replace(tzinfo = pytz.utc)

class ArticleListView(ListView):
    model = Event
    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context["dt_now"] = get_now()
        return context
      
    def get_queryset( self ):
      qs = self.model.objects.filter( close__gt = get_now() ).order_by('open','close')[0:10]
      return qs

def format_time( dt ):
  return dt.isoformat()
  
def json_feed(request):
  # Get next 10 openening up chats
  qs = Event.objects.filter( close__gt = get_now() ).order_by('open','close')[0:10]
  json_ret = []
  for e in qs.values('open','close','url','desc', 'chat__name', 'chat__desc', 'chat__url'):
    
     json_ret.append( { 'open'  : format_time( e['open'] ),
                        'close' : format_time( e['close'] ),
                        'name'  : e['chat__name'],
                        'url'   : (e['url'] if e['url'] else e['chat__url']),
                        'desc'  : (e['desc'] if e['desc'] else e['chat__desc']),
                      } )
  return HttpResponse( json.dumps(json_ret) )