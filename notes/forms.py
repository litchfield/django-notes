from datetime import datetime, timedelta
from django import forms
from django.forms.models import BaseModelFormSet
from django.conf import settings
from django.contrib.contenttypes.generic import generic_inlineformset_factory, BaseGenericInlineFormSet
from models import Note
from widgets import ReminderWidget

class SnoozeForm(forms.Form):
    snooze = forms.DateTimeField(widget=ReminderWidget)
    
    def clean_snooze(self):
        s = self.cleaned_data.get('snooze')
        if s < datetime.now():
            raise forms.ValidationError("Date/time is in the past (%s time)" % settings.TIME_ZONE)
        return s
    
class ReminderAdminForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('content_type', 'object_id')
        widgets = {
            'reminder': ReminderWidget,
        }    

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        widgets = {
            'reminder': ReminderWidget,
        }

class LockoutFormSetMixin(object):
    allow_change_within = getattr(settings, 'NOTES_ALLOW_CHANGE_WITHIN', 30)  # Allow notes to be edited by same user with X minutes
    
    def __init__(self, user=None, instance=None, **kwargs):
        self.user = user
        super(LockoutFormSetMixin, self).__init__(instance=instance, **kwargs)
        for form in self.forms:
            form.can_edit = False
            form.can_delete = False
            if not form.instance.pk:
                form.can_edit = True
                continue
            cutoff = datetime.now() - timedelta(minutes=self.allow_change_within)
            if user.is_superuser or (user == instance.user and instance.created > cutoff):
                form.can_delete = True
                form.can_edit = True
        self.user = user
    
    def save_new(self, form, commit=True):
        obj = super(LockoutFormSetMixin, self).save_new(form, commit=False)
        obj.user = self.user
        if commit:
            obj.save()
        return obj
    
class BaseNoteFormSet(LockoutFormSetMixin, BaseGenericInlineFormSet):
    def total_form_count(self):
        self.extra = 0
        if self.user.is_staff:
            self.extra = 1
        return super(BaseNoteFormSet, self).total_form_count()
        
NoteFormSet = generic_inlineformset_factory(Note, form=NoteForm, formset=BaseNoteFormSet)