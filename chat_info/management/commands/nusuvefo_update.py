 
from django.core.management.base import BaseCommand, CommandError
import chat_info.models
import chat_event.models
import chat_event.run_fetch

import icalendar
import dateutil.rrule
import datetime
import pytz


def get_events_for( event, chat, now ):
   uid = event["UID"].strip()
   if event["DTSTART"].dt > now:
     retlist = [ chat_event.models.Event( 
                         open  = event["DTSTART"].dt,
                         close = event["DTEND"].dt,
                         uid   = uid,
                         chat  = chat ) ]
   else:
     retlist = []
   
   try:
      rule = dateutil.rrule.rrulestr( event["RRULE"].to_ical(), dtstart=event["DTSTART"].dt )
   except KeyError:
      return retlist
    
     
   duration = event["DTEND"].dt - event["DTSTART"].dt
   eventwindow = datetime.timedelta(weeks=2)
       
   dates = rule.between( now, now + eventwindow )
   
   if dates == None:
     return retlist
   
   for date in dates:
      retlist.append( chat_event.models.Event( 
                         open  = date,
                         close = date + duration,
                         uid   = uid,
                         chat  = chat ))
   return retlist   



class Command(BaseCommand):
    help = 'Does update for all the registered calenders'

    def handle(self, *args, **options):
      
      if len(args)  > 0 :
         raise CommandError('This command accepts no paramters')
      
      fetcher = chat_event.run_fetch.Nusu()
      fetcher.login()
      
      events_to_create = []
      now = (datetime.datetime.utcnow().replace( tzinfo=pytz.utc))
      
      for chat in chat_info.models.Chat.objects.all():
         ical_str = fetcher.get_ical( chat.remote_id )
         ical = icalendar.Calendar.from_ical( ical_str )
         
         for event in ical.walk("vevent"):
            events_to_create.extend( get_events_for( event, chat, now ) )
            
            
      # for simplicity we sacrifice performance,:
      # drop all & make all rather than update + that 
             
      chat_event.models.Event.objects.all().delete()
      chat_event.models.Event.objects.bulk_create( events_to_create )
      
