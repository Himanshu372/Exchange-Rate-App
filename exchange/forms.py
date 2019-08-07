# make sure this is at the top if it isn't already
from django import forms

# our new form
class ExchangeRateForm(forms.Form):
    base_curr = forms.CharField(max_length = 3, required=True)
    target_curr = forms.CharField(max_length = 3, required=True)
    amount = forms.CharField(required=True)
    max_wait_time = forms.CharField(max_length = 10, required=True)
    start_date = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'})
    )