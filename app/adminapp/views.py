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

    
class VillageListView(View):
    def get(self, request, *args, **kwargs):
        puskesmas = request.user
        villages = Village.objects.filter(puskesmas=puskesmas).order_by("-created_at")
        context = {
            "villages": villages
        }
        return render(request, "adminapp/village_list.html", context)
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get("form-action")
        match action:
            case "add": self.add_village(request)
            case "edit": self.edit_village(request)
            case "delete": self.delete_village(request)
        return redirect("village_list") 
    
    def add_village(self, request):
        name = request.POST.get("village-name")
        village = Village.objects.create(
            puskesmas=request.user,
            name=name
        )
        messages.success(request, "Desa berhasil ditambahkan")
        return redirect("village_list") 
    
    def delete_village(self, request):
        village_id = request.POST.get("pk")
        village = Village.objects.filter(id=village_id).first()
        if village is not None:
            village.delete()
            messages.success(request, "Desa berhasil dihapus")
        return redirect("village_list")
    
    def edit_village(self, request):
        village_id = request.POST.get("pk")
        name = request.POST.get("village-name")
        village = Village.objects.filter(id=village_id).first()
        if village is not None:
            village.name = name
            village.save()
            messages.success(request, "Desa berhasil diubah")
        return redirect("village_list")

