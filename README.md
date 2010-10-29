Django Notes
============


Overview
--------

Easily add notes and basic reminders to your django apps.

Reminders popup at the bottom of the screen using ajax.

Requires Django 1.2+.


Instructions
------------

1. Add notes to your PYTHONPATH and INSTALLED_APPS

2. If you wish to use notes in admin, add "notes" from notes/media to your MEDIA_URL (or settings.NOTES_MEDIA_URL).

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

The following settings are supported via settings.py (all optional) --

- Popup reminders NOTES_REMINDER minutes in advance (default 15). Zero to disable.
- Popups refresh every NOTES_INTERVAL minutes (default 1)
- Allow edits for non superusers within NOTES_ALLOW_CHANGE_WITHIN minutes of posting (default 30). Zero to disable.
- NOTES_MEDIA_URL if you need the supplied admin media files coming from somewhere other than MEDIA_URL.

