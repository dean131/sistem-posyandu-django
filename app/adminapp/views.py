from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from account.models import (
    Puskesmas,
)

from base.models import (
    Village,
    Child
)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        next_page = request.GET.get('next', '/')
        if request.user.is_authenticated:
            # Redirect to previous page or home page
            return redirect(next_page if next_page != '/login/' else '/')
        return render(request, "adminapp/auth_login.html")
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = Puskesmas.objects.filter(email=email).first()
        if user is not None and user.role == "PUSKESMAS":
            is_password_valid = user.check_password(password)
            if is_password_valid:
                login(request, user)
                return redirect("dashboard")
        
        messages.error(request, "Email atau password salah")
        return redirect("login")
    

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        children = Child.objects.filter(
            parent__address__subdistrict=request.user.address.subdistrict
        ).count()
        context = {
            "children": children
        }
        return render(request, "adminapp/dashboard.html", context)

    
# class VillageListView(View):
#     def get(self, request, *args, **kwargs):
#         puskesmas = request.user
#         villages = Village.objects.filter(puskesmas=puskesmas)
#         context = {
#             "villages": villages
#         }
#         return render(request, "adminapp/village_list.html", context)
