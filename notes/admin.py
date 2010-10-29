from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib import messages
from django.contrib.admin.util import unquote
from django.utils.functional import curry
from models import Note
from forms import *

class BaseNoteAdmin(admin.ModelAdmin):
    "Adds notes to any admin"
    change_form_template = 'admin/change_form_notes.html'

    def get_form(self, request, obj=None, **kwargs):
        modeladmin = self
        ModelForm = self.form
        class NoteAdminForm(ModelForm):
            def is_valid(self):
                valid = super(NoteAdminForm, self).is_valid()
                if valid and hasattr(modeladmin, 'noteformset'):
                    valid = modeladmin.noteformset.is_valid()
                return valid
        self.form = NoteAdminForm
        return super(BaseNoteAdmin, self).get_form(request, obj, **kwargs)
        
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        noteformset = context.get('noteformset')
        if noteformset:
            errors = context['errors']
            errors.extend(noteformset.non_form_errors())
            for e in noteformset.errors:
                errors.extend(e.values())
        return super(BaseNoteAdmin, self).render_change_form(request, context, add, change, form_url, obj)
        
    def change_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, unquote(object_id))
        noteformset = NoteFormSet(user=request.user, data=request.POST or None,
                                  instance=obj, queryset=obj.notes.all())
        if noteformset.is_valid():
            noteformset.save()
            change_message = self.construct_change_message(request, forms.Form(), [noteformset])
            self.log_change(request, obj, change_message)
        self.noteformset = noteformset
        extra_context = extra_context or {}
        extra_context['noteformset'] = noteformset
        return super(BaseNoteAdmin, self).change_view(request, object_id, extra_context)

class ReminderAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'reminder', '__unicode__')
    form = ReminderAdminForm
    
    def has_add_permission(self, request):
        return False
        
    def queryset(self, request):
        return Note.objects.filter(user=request.user).exclude(reminder=None)
    
    def __unicode__(self):
        return 'Reminder'
        
admin.site.register(Note, ReminderAdmin)
