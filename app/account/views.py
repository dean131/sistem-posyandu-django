from pyexpat.errors import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from account.models import Midwife, Cadre, Parent, Puskesmas, User
from village.models import Village
from posyandu.models import Posyandu
from child.models import Child
from account.forms import AssignVillageToMidwifeForm, AssignPosyanduToCadreForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        next_page = request.GET.get("next", "/")
        if request.user.is_authenticated:
            # Redirect to previous page or home page
            return redirect(next_page if next_page != "/login/" else "/")
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


@method_decorator(login_required(login_url="login"), name="dispatch")
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        # Queries to count the relevant data
        children_count = Child.objects.count()
        parents_count = Parent.objects.count()
        midwives_count = Midwife.objects.count()
        cadres_count = Cadre.objects.count()

        # Context data for the dashboard
        context = {
            "children": children_count,
            "parents": parents_count,
            "midwives": midwives_count,
            "cadres": cadres_count,
        }

        return render(request, "adminapp/dashboard.html", context)


class MidwifeListView(View):
    template_name = "midwife/midwife_list.html"

    def get(self, request, *args, **kwargs):
        if (
            request.headers.get("x-requested-with") == "XMLHttpRequest"
        ):  # Check for AJAX request
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            search_value = request.GET.get("search[value]", "")

            queryset = Midwife.objects.all()
            if search_value:
                queryset = queryset.filter(full_name__icontains=search_value)

            total = queryset.count()
            data = []

            for midwife in queryset[start : start + length]:
                data.append(
                    {
                        "id": str(midwife.id),
                        "full_name": midwife.full_name,
                        "whatsapp": midwife.whatsapp,
                        "villages": ", ".join(
                            [village.name for village in midwife.villages.all()]
                        ),
                    }
                )

            return JsonResponse(
                {
                    "draw": draw,
                    "recordsTotal": total,
                    "recordsFiltered": total,
                    "data": data,
                }
            )

        return render(request, self.template_name)


class AssignVillageToMidwifeView(UpdateView):
    model = Midwife
    form_class = AssignVillageToMidwifeForm
    template_name = "midwife/assign_village.html"
    success_url = reverse_lazy("midwife_list")

    def get_initial(self):
        initial = super().get_initial()
        midwife = self.get_object()
        initial["villages"] = midwife.villages.all()
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Desa berhasil diperbarui untuk bidan ini.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Terjadi kesalahan saat memperbarui desa.")
        return super().form_invalid(form)

    def get_queryset(self):
        return Midwife.objects.all()


class CadreListView(TemplateView):
    template_name = "cadre/cadre_list.html"

    def get(self, request, *args, **kwargs):
        # Handle AJAX request for DataTable
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            search_value = request.GET.get("search[value]", "").strip()
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_column_name = request.GET.get(f"columns[{order_column_index}][data]")
            order_dir = request.GET.get("order[0][dir]", "asc")

            cadres = Cadre.objects.prefetch_related("cadre_posyandus").all()

            # Apply search filter
            if search_value:
                cadres = cadres.filter(full_name__icontains=search_value)

            # Apply sorting
            if order_column_name:
                order_column_name = (
                    f"-{order_column_name}"
                    if order_dir == "desc"
                    else order_column_name
                )
                cadres = cadres.order_by(order_column_name)

            total_records = cadres.count()
            cadres = cadres[start : start + length]

            # Format data for DataTable
            data = [
                {
                    "id": str(cadre.id),
                    "full_name": cadre.full_name,
                    "whatsapp": cadre.whatsapp,
                    "posyandus": ", ".join(
                        posyandu.name for posyandu in cadre.cadre_posyandus.all()
                    ),
                }
                for cadre in cadres
            ]

            return JsonResponse(
                {
                    "draw": int(request.GET.get("draw", 0)),
                    "recordsTotal": total_records,
                    "recordsFiltered": total_records,
                    "data": data,
                }
            )

        return super().get(request, *args, **kwargs)


# class AssignPosyanduToCadreView(View):
#     def get(self, request, pk, *args, **kwargs):
#         cadre = get_object_or_404(Cadre, pk=pk)
#         posyandus = Posyandu.objects.all()
#         return render(
#             request,
#             "cadre/assign_posyandu.html",
#             {"cadre": cadre, "posyandus": posyandus},
#         )

#     def post(self, request, pk, *args, **kwargs):
#         cadre = get_object_or_404(Cadre, pk=pk)
#         posyandu_ids = request.POST.getlist("posyandus")
#         cadre.cadre_posyandus.set(posyandu_ids)
#         messages.success(request, "Posyandu berhasil diperbarui untuk kader ini.")
#         return redirect("cadre_list")


class AssignPosyanduToCadreView(UpdateView):
    model = Cadre
    form_class = AssignPosyanduToCadreForm
    template_name = "cadre/assign_posyandu.html"
    success_url = reverse_lazy("cadre_list")

    def get_initial(self):
        # Get initial data for the form
        initial = super().get_initial()
        cadre = self.get_object()
        initial["cadre_posyandus"] = cadre.cadre_posyandus.all()
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Posyandu berhasil diperbarui untuk kader ini.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Terjadi kesalahan saat memperbarui posyandu.")
        return super().form_invalid(form)

    def get_queryset(self):
        # Return all Cadre objects
        return Cadre.objects.all()
