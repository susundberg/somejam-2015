from django.db import models
import chat_info.models

class Event(models.Model):
  open  = models.DateTimeField( verbose_name="When chat opens")
  close = models.DateTimeField( verbose_name="When chat closes")
  chat  = models.ForeignKey( chat_info.models.Chat, verbose_name="For what chat")  
  url   = models.CharField( max_length = 255, verbose_name= "Target url for the chat", blank = True, null=True )
  desc  = models.CharField( max_length = 255, verbose_name= "Special title for the chat", blank = True, null=True )
  
  def __unicode__(self):
    return unicode( self.chat ) + ": %s to %s " % ( self.open ,self.close )
  
