from datetime import datetime
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from django.conf import settings

class Note(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey()

    text = models.TextField()
    created = models.DateTimeField(editable=False, default=datetime.now)
    user = models.ForeignKey('auth.User', null=True, blank=True, editable=False, related_name='notes')
    reminder = models.DateTimeField(null=True, blank=True, verbose_name='reminder time')
    
    def __unicode__(self):
        return self.text[:50]

    @models.permalink
    def get_admin_url(self):
        obj = self.content_object
        if not obj:
            return
        ct = ContentType.objects.get_for_model(obj.__class__)
        return ("admin:%s_%s_change" % (ct.app_label, ct.model), [obj.pk])
    
class NotesField(generic.GenericRelation):
    def __init__(self, **kwargs):
        super(ModelNotes, self).__init__(Note, **kwargs)