from django.shortcuts import render
from login_app.forms import UserForm, UserInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.contrib.auth.models import User
from login_app.models import UserInfo
# Create your views here.

def index(request):
    diction = {'title':"Home"}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk = user_id)
        user_more_info = UserInfo.objects.get(user__pk = user_id) #for relational database we use (base model__pk=usier id)
        diction.update({'user_basic_info':user_basic_info, 'user_more_info':user_more_info})
        # print(current_user.username)
        # print(current_user.email)
        # print(current_user.id)
        # print(request)
    return render(request, 'login_app/index.html', context=diction)

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False) #commt false will not update the database
            user_info.user = user

            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']

            user_info.save()
            registered = True
    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    diction = {'user_form':user_form, 'user_info_form': user_info_form, 'registered':registered}
    return render(request, 'login_app/register.html', context=diction)


def login_page(request):
    return render(request, 'login_app/login.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('login_app:index'))
            else:
                return HttpResponse("Account is not active!")

        else:
            return HttpResponse("Login Details are Wrong!")

    else:
        # return render(request, 'login_app/login.html', context={})
        return HttpResponseRedirect(reverse('login_app:login'))


@login_required #it checks if the user has loged in or not.
# If the user staus is login then the user_logout will call otherwise not
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_app:index'))
