from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


import chat_event.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nettiapuanyt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', chat_event.views.ArticleListView.as_view()),
)
