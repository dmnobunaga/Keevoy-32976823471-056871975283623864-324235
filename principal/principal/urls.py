from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # :
                       url(r'^$', 'principal.views.main', name='main'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
)
