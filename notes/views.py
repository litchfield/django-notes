from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.dateformat import format
from models import Note
from forms import SnoozeForm

REMINDER = getattr(settings, 'NOTES_REMINDER', 15)  # minutes ahead to remind

def get_reminder_html(user):
    cutoff = datetime.now() + timedelta(minutes=REMINDER)
    reminders = Note.objects.filter(user=user, reminder__lte=cutoff)
    form = SnoozeForm()
    return render_to_string('admin/ajax_reminders.html', locals())
    
def ajax_reminders(request):
    html = get_reminder_html(request.user)
    return HttpResponse(html)

def reminder_action(request):
    try:
        note = Note.objects.get(id=request.GET.get('id'))
        assert note.reminder is not None
    except:
        note = None
    if note:
        action = request.GET.get('action')
        if action == 'dismiss':
            note.reminder = None
            note.save()
            messages.success(request, 'Dismissed reminder on %s' % str(note.content_object))
        elif action == 'snooze':
            form = SnoozeForm(data=request.GET)
            if form.is_valid():
                new = form.cleaned_data['snooze']
                note.reminder = new
                note.save()
                s = format(new, "P, l jS F")
                messages.success(request, 'Snoozed reminder for %s to %s' % (str(note.content_object), s))
            else:
                msg = ', '.join(form.errors.get('snooze'))
                messages.error(request, "Can't snooze. " + msg)
    else:
        messages.warning(request, 'Invalid reminder.')
    url = request.GET.get('url', request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(url)
