from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, get_backends, login, logout

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

from yamaha_amc_app.EmailBackEnd import EmailBackEnd


def showDemoPage(request):
    return render(request, 'demo.html')

def ShowLoginPage(request):
    return render(request, "login_page.html")

def do_Login(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        user = EmailBackEnd.authenticate(
            request, username=request.POST.get('email'), password=request.POST.get('password')
        )
        
        if user is not None:
            user.backend = 'yamaha_amc_app.EmailBackEnd.EmailBackEnd'
            
            login(request, user)
            if user.user_type == '1':
                return HttpResponseRedirect(("/admin_home"))
            elif user.user_type == '2':
                return HttpResponseRedirect(reverse('trainer_home'))
            elif user.user_type == '3':
                return HttpResponseRedirect(reverse('customer_home'))
            else:
                messages.error(request, "You are not a Gym Member")
                return render(request, "login_page.html")
        else:
            messages.error(request, "You are not a Gym Member")
            return render(request, "login_page.html")
        
def Logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
