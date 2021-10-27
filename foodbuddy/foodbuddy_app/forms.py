from django import forms

# This code is not being used right now. But this file might be used later to create forms via Django.
class ModifyForm(forms.Form):
    Start_Date=forms.DateField(label='Start Date')
    End_Date=forms.DateField(label='End Date')
    Start_Time=forms.TimeField(label='Start Time')
    End_Time=forms.TimeField(label='End Time')
    Party=forms.IntegerField(label='Number of people',min_value=1)