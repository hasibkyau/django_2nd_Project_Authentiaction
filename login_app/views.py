from django.shortcuts import render
from login_app.forms import UserForm, UserInfoForm
# Create your views here.

def index(request):
    diction = {'title':"Home"}
    return render(request, 'login_app/index.html', context=diction)

def register(request):
    user_form = UserForm()
    user_info_form = UserInfoForm()
    diction = {'user_form':user_form, 'user_info_form': user_info_form}
    return render(request, 'login_app/register.html', context=diction)
