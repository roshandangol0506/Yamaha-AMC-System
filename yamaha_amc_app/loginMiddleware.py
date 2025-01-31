from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        if request.path.startswith(settings.STATIC_URL) or request.path.startswith(settings.MEDIA_URL):
            return None 
        
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "yamaha_amc_app.HodViews" or modulename == "yamaha_amc_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "yamaha_amc_app.TrainerViews" or modulename == "yamaha_amc_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("trainer_home"))
            elif user.user_type == "3":
                if modulename == "yamaha_amc_app.CustomerViews" or modulename == "yamaha_amc_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("customer_home"))
            else:
                return HttpResponseRedirect(reverse("ShowLoginPage"))
        else:
            if request.path == reverse("ShowLoginPage") or request.path == reverse("do_login") or modulename == 'django.contrib.auth.views':
                pass
            else:
                return HttpResponseRedirect(reverse("ShowLoginPage"))
