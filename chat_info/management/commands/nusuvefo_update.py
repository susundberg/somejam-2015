 
from django.core.management.base import BaseCommand, CommandError
import chat_info.models
import chat_event.models
import chat_event.run_fetch

import icalendar


class Command(BaseCommand):
    help = 'Does update for all the registered calenders'

    def handle(self, *args, **options):
      
      if len(args)  > 0 :
         raise CommandError('This command accepts no paramters')
      
      fetcher = chat_event.run_fetch.Nusu()
      fetcher.login()
      
      events_to_create = []
      
      for chat in chat_info.models.Chat.objects.all():
         ical_str = fetcher.get_ical( chat.remote_id )
         ical = icalendar.Calendar.from_ical( ical_str )
         
         for event in ical.walk("vevent"):
            to_add = chat_event.models.Event( 
                    open  = event.get("dtstart").dt,
                    close = event.get("dtend").dt,
                    uid   = event.get("uid").strip(),
                    chat  = chat )
            events_to_create.append( to_add )
            
      # for simplicity we sacrifice performance,:
      # drop all & make all rather than update + that 
             
      chat_event.models.Event.objects.all().delete()
      chat_event.models.Event.objects.bulk_create( events_to_create )
      
