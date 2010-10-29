from datetime import date, datetime, time, timedelta
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
            choices += [ (d, d.strftime('%d %m %Y')) ]
        self.choices = choices

class ReminderTimeWidget(forms.Select):
    def __init__(self, attrs={}, format=None):
        super(ReminderTimeWidget, self).__init__(attrs=attrs)
        choices = [('', '--------')]
        for hour in range(8, 20):
            choices += [ (time(hour, 0), '%02d:00' % hour) ]
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
