from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       # :
                       url(r'^$', 'principal.views.main', name='main'),
                       url(r'registration', 'principal.views.registration', name='registration'),
                       url(r'create_user', 'principal.views.create_user', name='create_user'),

                       url(r'login', 'principal.views.user_login', name='user_login'),
                       url(r'cabinet/$', 'principal.views.cabinet', name='cabinet'),
                       url(r'cabinet/campaign/$', 'principal.views.campaign', name='campaign'),
                       url(r'cabinet/campaign/save$', 'principal.views.campaign_save', name='campaign_save'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       # Yandex Money
                       url(r'^fail-payment/$', TemplateView.as_view(template_name='fail.html'), name='payment_fail'),
                       url(r'^success-payment/$', TemplateView.as_view(template_name='success.html'),
                           name='payment_success'),
                       url(r'^yandex-money/', include('yandex_money.urls'))
                       )
