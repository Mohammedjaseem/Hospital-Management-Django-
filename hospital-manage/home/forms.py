from django import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models  

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'booking_date': DateInput()
        }
        labels = {
            'p_name': 'Patient Name',
            'p_phone': 'Patient Phone',
            'p_email': 'Patient Email',
            'doc_name': 'Doctor',
            'booking_date': 'Booking Date',
        }

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)  

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user



