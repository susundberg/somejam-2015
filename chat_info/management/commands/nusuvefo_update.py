 
from django.core.management.base import BaseCommand, CommandError
import chat_info.models
import chat_event.models
import chat_event.run_fetch

  
class Command(BaseCommand):
    help = 'Does update for all the registered calenders'
    
    def handle(self, *args, **options):
      
      if len(args)  > 0 :
         raise CommandError('This command accepts no paramters')
      
      fetcher = chat_event.run_fetch.Provider()
      fetcher.login()
      
      events_to_create = []
      for chat in chat_info.models.Chat.objects.all():
         event_list = fetcher.get_calender_events( chat.remote_id )
         for event in event_list:
            events_to_create.append( chat_event.models.Event( open = event[1], close=event[2], chat=chat ) )
            
      # for simplicity we sacrifice performance,:
      # drop all & make all rather than update + that 
      chat_event.models.Event.objects.all().delete()
      chat_event.models.Event.objects.bulk_create( events_to_create )
      
