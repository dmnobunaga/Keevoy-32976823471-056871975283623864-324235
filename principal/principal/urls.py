from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # :
                       url(r'^$', 'principal.views.main', name='main'),
                       url(r'registration', 'principal.views.registration', name='registration'),
                       url(r'create_user', 'principal.views.create_user', name='create_user'),

                       url(r'login', 'principal.views.user_login', name='user_login'),
                       url(r'cabinet/', 'principal.views.cabinet', name='cabinet'),
                       url(r'campaign/$', 'principal.views.campaign', name='campaign'),
                       url(r'campaign/save$', 'principal.views.campaign_save', name='campaign_save'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
)
