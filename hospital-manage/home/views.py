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
from .forms import Booking 
from .forms import Doctors
from .forms import DoctorsAddforms

def index(request):
    return render(request, 'index.html') 

def about(request):
    return render(request, 'about.html')

def bookings(request):
	if request.user.is_authenticated:
    			if request.method == 'POST':
    			    form = BookingForm(request.POST, request.FILES) # request.FILES is used to upload files
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
		messages.success(request, "You need to login for bookings" )
		return redirect("login")
	messages.success(request, "Something Went Wrong please try again" )
	return redirect("login")
		



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
			# login(request, user) this will make user login automatically before a manuel login 
			
			messages.success(request, "Registration successful, Please Login" )
			return redirect("login")
			
            # add a else case for wrong login details 
		else:
			messages.error(request,"Unsuccessful registration. Invalid information.")
			return redirect("register")
		messages.error(request, "Unsuccessful registration. Invalid information.")
		return redirect("register")
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
				# messages.info(request, f"You are now logged in as {username}.")  # this will display a message on the screen after login
				return redirect("profile")
			else:
				messages.error(request,"Invalid username or password.")
				return redirect("login")
		else:			
			messages.error(request,"Invalid username or password.")
			return redirect("login")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")
	

def profile(request):
	if request.user.is_authenticated:
		return render(request, "profile.html")
	else:
		return redirect("login")


def viewbookings(request):
	if request.user.is_superuser:
		dic_dept={
        'dept': Booking.objects.all()
		}
		
		return render(request, "viewbookings.html",dic_dept )

	else:
		messages.error(request, "You are not authorized to view this page")
		return redirect("login")

def adddoctors(request):
	if request.user.is_authenticated:
    			if request.method == 'POST':
    			    form = DoctorsAddforms(request.POST, request.FILES) # request.FILES is used to upload files
    			    if form.is_valid():
    			        form.save()
    			        return render(request, 'confrm.html')
					
    			else:       
    			    DoctorsAdd = DoctorsAddforms()
    			    dict_form = {
    			        'form': DoctorsAdd
    			    }
    			    return render(request, 'adddoctors.html', dict_form)
				
	messages.success(request, "Only Super User can add a doctor" )
	return redirect("login")
		












