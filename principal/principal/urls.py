from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       # :
                       url(r'^$', 'principal.views.main', name='main'),
                       url(r'^mobile$', 'principal.views.mobile', name='mobile'),
                       url(r'registration', 'principal.views.registration', name='registration'),
                       url(r'create_user', 'principal.views.create_user', name='create_user'),

                       url(r'login', 'principal.views.user_login', name='user_login'),
                       url(r'logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
                       url(r'cabinet/$', 'principal.views.cabinet', name='cabinet'),
                       url(r'cabinet/billing$', 'principal.views.billing', name='billing'),
                       url(r'cabinet/faq', 'principal.views.faq', name='faq'),
                       url(r'cabinet/campaign/$', 'principal.views.campaign', name='campaign'),
                       url(r'cabinet/campaign/save$', 'principal.views.campaign_save', name='campaign_save'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       # Yandex Money
                       url(r'^cabinet/payment/$', 'principal.views.payment_yandex', name='payment_yandex'),
                       url(r'^fail-payment/$', TemplateView.as_view(template_name='fail.html'), name='payment_fail'),
                       url(r'^success-payment/$', TemplateView.as_view(template_name='success.html'),
                           name='payment_success'),
                       url(r'^yandex-money/', include('yandex_money.urls')),

                        #Help Desk
                       (r'cabinet/support/', include('helpdesk.urls')),

                       )
