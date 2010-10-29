Django Notes
============


Overview
--------

Easily add notes and basic reminders to your django apps.

Reminders popup at the bottom of the screen using ajax.

Requires jquery.


Instructions
------------

1. Add notes to your PYTHONPATH and INSTALLED_APPS

2. Give your models notes. Example --

	from notes import NotesField
    
	class MyModel(models.Model):
		...
		notes = NotesField()
		...

3. Show notes in admin (at the bottom). Example --

	from notes import BaseNoteAdmin
    
	class MyAdmin(BaseNoteAdmin):
		...

4. Use NoteFormSet in your views. Example --

    formset = NoteFormSet(user=request.user, data=request.POST)


Settings
--------

- Popup reminders NOTES_REMINDER minutes in advance (default 15)
- Allow edits for non superusers within NOTES_ALLOW_CHANGE_WITHIN minutes of posting (default 30)