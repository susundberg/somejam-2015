from django.db import models


class ChatType(models.Model):
  name = models.CharField(max_length=64, verbose_name="Short description of the the type")
  
  def __unicode__(self):
    return self.name 
  
class Chat(models.Model):
    name       = models.CharField(max_length=64, verbose_name="Short description of the chat. Will be used for matching of the ICAL name")
    explain    = models.TextField(verbose_name="Longer description of the chat")
    type       = models.ForeignKey( 'ChatType', verbose_name="What kind of chat is it")
    remote_id  = models.PositiveSmallIntegerField( verbose_name="What is the remote ID of the calender", unique=True)
    
    def __unicode__(self):
      return self.name 


