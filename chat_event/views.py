from django.views.generic.list import ListView

from chat_event.models import Event

class ArticleListView(ListView):
    model = Event
    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        return context
    def get_queryset( self ):
      qs = self.model.objects.all().order_by('open','close')[0:10]
      return qs
    