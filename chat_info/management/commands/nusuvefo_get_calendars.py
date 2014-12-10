 
from django.core.management.base import BaseCommand, CommandError
import chat_info.models
import chat_event.run_fetch

import icalendar


class Command(BaseCommand):
    help = 'Does update for all the registered calenders'

    def handle(self, *args, **options):
      
      if len(args)  > 0 :
         raise CommandError('This command accepts no paramters')
      
      fetcher = chat_event.run_fetch.Provider()
      fetcher.login()
      chat_type = chat_info.models.ChatType.objects.get( name="Unknown type")
      
      cals_to_create = []
      cals_found = fetcher.get_calendenders()
      for (cal_name, cal_id) in cals_found :
          chat_info.models.Chat.objects.get_or_create(
                  name = cal_name,
                  remote_id = cal_id,
                  defaults = {
                     'type'    : chat_type,
                     'url'     : 'http://www.google.com',
                     'desc'    : 'Automatically fetched, replace me!',
                     }
                  )
