from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Village


class VillageListView(View):
    def get(self, request, *args, **kwargs):
        # Check if it's an AJAX request for DataTables
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return self.get_villages_data(request)

        # Render the main template
        return render(
            request,
            "village/village_list.html",
        )

    def get_villages_data(self, request):
        # Get DataTables parameters
        draw = int(request.GET.get("draw", 0))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()
        order_column_index = int(request.GET.get("order[0][column]", 0))
        order_direction = request.GET.get("order[0][dir]", "asc")

        # Map DataTables columns to model fields
        columns = ["id", "id", "name"]
        order_column = columns[order_column_index]
        if order_direction == "desc":
            order_column = f"-{order_column}"

        # Get the logged-in user's Puskesmas
        puskesmas = request.user

        # Filter data based on search value
        queryset = Village.objects.filter(puskesmas=puskesmas)
        if search_value:
            queryset = queryset.filter(Q(name__icontains=search_value))

        # Total records and filtered records
        total_records = queryset.count()
        filtered_records = queryset.count()

        # Apply ordering and pagination
        queryset = queryset.order_by(order_column)[start : start + length]

        # Prepare data for DataTables
        data = [
            {
                "id": village.id,
                "name": village.name,
            }
            for village in queryset
        ]

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": filtered_records,
                "data": data,
            }
        )


class VillageCreateView(CreateView):
    model = Village
    fields = ["name"]  # Fields to include in the form
    template_name = "village/village_create_form.html"  # Template for the form
    success_url = reverse_lazy("village_list")  # Redirect after success

    def form_valid(self, form):
        form.instance.puskesmas = (
            self.request.user
        )  # Assuming puskesmas is the current user
        messages.success(self.request, "Desa berhasil ditambahkan.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Terjadi kesalahan saat menambahkan desa.")
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({"class": "form-control"})
        return form


class VillageUpdateView(UpdateView):
    model = Village
    fields = ["name"]  # Fields to include in the form
    template_name = "village/village_update_form.html"  # Reuse the form template
    success_url = reverse_lazy("village_list")  # Redirect after success

    def form_valid(self, form):
        messages.success(self.request, "Desa berhasil diperbarui.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Terjadi kesalahan saat memperbarui desa.")
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({"class": "form-control"})
        return form


class VillageDeleteView(DeleteView):
    model = Village
    template_name = "village/village_confirm_delete.html"  # Confirmation template
    success_url = reverse_lazy("village_list")  # Redirect after success

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Desa berhasil dihapus.")
        return super().delete(request, *args, **kwargs)
