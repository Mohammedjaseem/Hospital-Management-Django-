from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm 


# Create your views here.
from .models import Departments
from .models import Doctors
from .forms import BookingForm



def index(request):
    return render(request, 'index.html') 

def about(request):
    return render(request, 'about.html')

def bookings(request):
	if request.user.is_authenticated:
    			if request.method == 'POST':
    			    form = BookingForm(request.POST)
    			    if form.is_valid():
    			        form.save()
    			        return render(request, 'confrm.html')
    			else:       
    			    form = BookingForm()
    			    dict_form = {
    			        'form': form
    			    }
    			    return render(request, 'bookings.html', dict_form)
	else:
		return redirect("warning")


def doctors(request):
    dic_docs = {
        'doctors': Doctors.objects.all()
    }
    return render(request, 'doctors.html', dic_docs)

def contact(request):
    return render(request, 'contact.html')

def department(request):
    dic_dept={
        'dept':Departments.objects.all()
    }
    return render(request, 'department.html', dic_dept)

# user adding
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

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("login")
            # add a else case for wrong login details 
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("profile")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")

def profile(request):
	if request.user.is_authenticated:
		return render(request, "profile.html")
	else:
		return redirect("login")

def warning(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("bookings")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="warning.html", context={"login_form":form})






