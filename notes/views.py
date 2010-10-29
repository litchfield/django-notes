from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.shortcuts import *
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponseNotFound
from models import Note
from forms import SnoozeForm

REMINDER = getattr(settings, 'NOTES_REMINDER', 15)  # minutes ahead to remind

def ajax_reminders(request):
    cutoff = datetime.now() + timedelta(minutes=REMINDER)
    reminders = Note.objects.filter(user=request.user, reminder__lte=cutoff)
    form = SnoozeForm()
    return render_to_response('admin/ajax_reminders.html', locals(), RequestContext(request))

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
            messages.success(request, 'Dismissed reminder on %s.' % str(note.content_object))
        elif action == 'snooze':
            form = SnoozeForm(data=request.GET)
            if form.is_valid():
                new = form.cleaned_data['snooze']
                note.reminder = new
                note.save()
                messages.success(request, 'Snoozed reminder for %s to %s' % (str(note.content_object), new))
            else:
                messages.warning(request, 'Invalid snooze time selected.')
    else:
        messages.warning(request, 'Invalid reminder.')
    url = request.GET.get('url', request.META.get('HTTP_REFERER'))
    initial_html = ajax_reminders(request).contents
    return HttpResponseRedirect(url)
