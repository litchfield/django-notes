from django import template
from django.conf import settings
from notes.views import get_reminder_html
register = template.Library()

INTERVAL = getattr(settings, 'NOTES_INTERVAL', 1)  # refresh every X minutes
MEDIA_URL = getattr(settings, 'NOTES_MEDIA_URL', settings.MEDIA_URL)

@register.inclusion_tag('admin/reminders.html')
def reminders(user):
    return {'initial_html': get_reminder_html(user),  
            'interval': INTERVAL,
            'MEDIA_URL': MEDIA_URL,
             }