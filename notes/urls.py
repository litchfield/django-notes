from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^ajax_reminders/', 'notes.views.ajax_reminders', name='ajax_reminders'),
    url(r'^reminder_action/', 'notes.views.reminder_action', name='reminder_action'),
)
