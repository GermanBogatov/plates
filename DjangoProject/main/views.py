from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .models import Note
from .forms import NoteForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

from django.views.generic.edit import CreateView
from .models import Note
from .forms import NoteForm
from .forms import UserLoginForm
from .forms import UserSignUpForm
from django.views import View
import pyotp
import time
from . import models

def check_pin_google(pin, secret_key):
    totp = pyotp.TOTP(secret_key)
    verification_status = totp.verify(pin)
    if verification_status:
        # return render(request, 'main/index.html', {'title': 'Главная страница сайта', 'notes': notes})
        return True
    else:
        # return render(request, 'main/index.html', {'title': 'Главная страница сайта'})
        return False

def index(request):
    notes = Note.objects.all()
    return render(request, 'main/index.html', {'title': 'Главная страница сайта', 'notes': notes})

@login_required(login_url='login_my')
def index(request):
    if request.method == 'GET':
        notes = Note.objects.all()
        #
        # u = User.objects.get(username='test')
        # johny_key = u.authinformation.secret_key
        #
        # auth_info_detail = models.AuthInformation.objects.first()
        # secret_key = auth_info_detail.secret_key
        # totp = pyotp.TOTP(secret_key)
        return render(request, 'main/index.html', {'title': f'Главная страница сайта', 'notes': notes})
    elif request.method == 'POST':
        return render(request, 'main/index.html', {'title': 'Главная страница сайта'})

def about(request):
    return render(request, 'main/about.html')

def register(request):
    form_class = UserCreationForm
    # success_url = reverse_lazy("login")
    return render(request, 'registration/signup.html', {'form': form_class})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            pin = request.POST['pin']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                key = user.secret_key
                if check_pin_google(pin, key):
                    auth.login(request, user)
                    return HttpResponseRedirect(reverse('home'))
    else:
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'registration/login.html', context)

def logout(request):
    return render(request, 'registration/logged_out.html')

def create(request):
    error = ''
    if request.method == 'POST': #здесь отправляем на сервак заметку
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            #form.save2()
            # form.getnote("b545d618-ff44-4319-9c88-2100d9928f32")
            # string = form.title + ';' + form.text
            return redirect('home')
        else:
            error = 'Форма была не верной'

    form = NoteForm()
    context ={
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', context)

# def create_user(request):
#     error = ''
#     if request.method == 'POST':
#         user = User.objects.create_user('myusernameme', 'myemail@crazymail.com', 'mypassword')
#         user.first_name = 'John'
#         user.last_name = 'Citizen'
#         user.save()
#         # acc = models.AuthInformation(secret_key='base32secret3111')
        # acc.secret_key = "base32secret3111"
        # user.authinformation = acc
        # user.authinformation.save()
        # tom = User.objects.create(username="Tom")
        # acc = models.AuthInformation(secret_key=pyotp.random_base32())
        # user.authinformation = acc
        # user.authinformation.save()

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def set_key(request):
    totp = pyotp.TOTP('base32secret3232')
    totp.now() # => '492039'
    # OTP verified for current time
    totp.verify('492039') # => True
    time.sleep(30)
    totp.verify('492039') # => False