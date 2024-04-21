from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from account.models import (
    Puskesmas,
    Parent,
    Midwife,
    Cadre,
)

from base.models import (
    Village,
    Child,
    Posyandu,
    MidwifeAssignment,
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
    

# @method_decorator(login_required(login_url='login'), name='dispatch')
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
        query = request.GET.get("q", "")
        puskesmas = request.user
        
        if query:
            villages = Village.objects.filter(
                puskesmas=puskesmas,
                name__icontains=query
            ).order_by("-created_at")
        else:
            villages = Village.objects.filter(
                puskesmas=puskesmas
            ).order_by("-created_at")

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
        Village.objects.create(
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
        else:
            messages.error(request, "Desa tidak ditemukan")
        return redirect("village_list")
    
    def edit_village(self, request):
        village_id = request.POST.get("pk")
        name = request.POST.get("village-name")
        village = Village.objects.filter(id=village_id).first()
        if village is not None:
            village.name = name
            village.save()
            messages.success(request, "Desa berhasil diubah")
        else:
            messages.error(request, "Desa tidak ditemukan")
        return redirect("village_list")


class VillageInfoView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        village = Village.objects.filter(id=pk).first()
        children = Child.objects.filter(
            parent__address__village=village.name
        )
        parents = Parent.objects.filter(
            address__village=village.name
        )
        posyandus = Posyandu.objects.filter(
            village=village
        )
        midwives = Midwife.objects.filter(
            midwifeassignment__village=village
        )
        context = {
            "village": village,
            "children": children,
            "parents": parents,
            "posyandus": posyandus,
            "midwives": midwives
        }
        return render(request, "adminapp/village_info.html", context) 


class PosyanduView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")

        if query:
            posyandus = Posyandu.objects.filter(
                village__puskesmas=request.user,
                name__icontains=query
            ).order_by("-created_at")
        else:
            posyandus = Posyandu.objects.filter(
                village__puskesmas=request.user
            ).order_by("-created_at")

        context = {
            "posyandus": posyandus 
        }
        return render(request, "adminapp/posyandu_page.html", context)
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get("form-action")
        match action:
            case "add": self.add_posyandu(request)
            case "edit": self.edit_posyandu(request)
            case "delete": self.delete_posyandu(request)
        return redirect("posyandu") 
    
    def add_posyandu(self, request):
        name = request.POST.get("posyandu-name")
        address = request.POST.get("posyandu-address")
        village_id = request.POST.get("village-id")
        village = Village.objects.filter(id=village_id).first()
        if village is not None:
            Posyandu.objects.create(
                name=name,
                address=address,
                village=village
            )
            messages.success(request, "Posyandu berhasil ditambahkan")
        else:
            messages.error(request, "Desa tidak ditemukan")
        return redirect("posyandu")
    
    def edit_posyandu(self, request):
        posyandu_id = request.POST.get("pk")
        name = request.POST.get("posyandu-name")
        address = request.POST.get("posyandu-address")
        village_id = request.POST.get("village-id")
        posyandu = Posyandu.objects.filter(id=posyandu_id).first()
        village = Village.objects.filter(id=village_id).first()
        if posyandu is not None:
            posyandu.name = name
            posyandu.address = address
            posyandu.village = village
            posyandu.save()
            messages.success(request, "Posyandu berhasil diubah")
        else:
            messages.error(request, "Posyandu tidak ditemukan")
        return redirect("posyandu")
    
    def delete_posyandu(self, request):
        posyandu_id = request.POST.get("pk")
        posyandu = Posyandu.objects.filter(id=posyandu_id).first()
        if posyandu is not None:
            posyandu.delete()
            messages.success(request, "Posyandu berhasil dihapus")
        else:
            messages.error(request, "Posyandu tidak ditemukan")
        return redirect("posyandu")
    

class MidwifeView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")

        if query:
            midwives = Midwife.objects.filter(
                full_name__icontains=query
            ).order_by("-created_at")
        else:
            midwives = Midwife.objects.filter().order_by("-created_at")

        context = {
            "midwives": midwives
        }
        return render(request, "adminapp/midwife.html", context)

class MidwifeInfoView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        midwife = Midwife.objects.filter(id=pk).first()
        context = {
            "midwife": midwife
        }
        return render(request, "adminapp/midwife_info.html", context)
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get("form-action")
        match action:
            case "delete": return self.delete_midwifeassignment(request)
        # return redirect("midwife_info", pk=midwife_id)
    
    def delete_midwifeassignment(self, request):
        midwifeassignment_id = request.POST.get("pk")
        midwifeassignment = MidwifeAssignment.objects.filter(id=midwifeassignment_id).first()
        if midwifeassignment is not None:
            midwifeassignment.delete()
            messages.success(request, "Bidan berhasil dihapus")
        else:
            messages.error(request, "Bidan tidak ditemukan")
        return redirect("midwife_info", pk=midwifeassignment.midwife.id)