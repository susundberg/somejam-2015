from django.db import models
import chat_info.models

class Event(models.Model):
  open  = models.DateTimeField( verbose_name="When chat opens")
  close = models.DateTimeField( verbose_name="When chat closes")
  chat  = models.ForeignKey( chat_info.models.Chat, verbose_name="For what chat")  
  uid   = models.CharField( max_length=32, verbose_name="identifier for the event from remote" )
  
  def __unicode__(self):
    return unicode( self.chat ) + ": %s to %s " % ( self.open ,self.close )
  
