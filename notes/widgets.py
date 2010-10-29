from datetime import date, datetime, time, timedelta
from django.utils.dateformat import format as date_format, time_format
from django import forms

class ReminderDateWidget(forms.Select):
    def __init__(self, attrs={}, format=None):
        super(ReminderDateWidget, self).__init__(attrs=attrs)
        choices = [
            ('', '--------'),
            (date.today(), 'Today'),
            (date.today() + timedelta(days=1), 'Tomorrow'),
        ]
        for offset in range(2, 15):
            d = date.today() + timedelta(days=offset)
            choices += [ (d, date_format(d, 'l jS')) ]
        self.choices = choices

class ReminderTimeWidget(forms.Select):
    def __init__(self, attrs={}, format=None):
        super(ReminderTimeWidget, self).__init__(attrs=attrs)
        choices = [('', '--------')]
        for hour in range(8, 20):
            choices += [ (time(hour, 0), time_format(time(hour, 0), 'P')) ]
        self.choices = choices
        
class ReminderWidget(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None):
        widgets = [ReminderDateWidget, ReminderTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

# class ReminderField(forms.DateTimeField):
#     widget = ReminderWidget
#     
#     def clean(self, value):
#         if value <= datetime.now():
#             raise forms.ValidationError(