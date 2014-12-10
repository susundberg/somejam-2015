from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


from django.views.generic.base import TemplateView

import chat_event.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nettiapuanyt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^html/list/',  TemplateView.as_view(template_name='html/list.html')),
    url(r'^json/v1/$', chat_event.views.json_feed),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^list/$', chat_event.views.ArticleListView.as_view()),
)
