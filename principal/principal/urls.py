from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # :
                       url(r'^$', 'principal.views.main', name='main'),
                       url(r'registration', 'principal.views.registration', name='registration'),
                       url(r'login', 'principal.views.login', name='login'),
                       url(r'cabinet/^$', 'principal.views.cabinet', name='cabinet'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
)
