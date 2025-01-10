from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Posyandu


class PosyanduListView(TemplateView):
    template_name = "posyandu/posyandu_list.html"

    def get(self, request, *args, **kwargs):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            draw = int(request.GET.get("draw", 0))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            search_value = request.GET.get("search[value]", "").strip()

            queryset = Posyandu.objects.select_related("village").all()

            if search_value:
                queryset = queryset.filter(name__icontains=search_value)

            total_records = queryset.count()
            queryset = queryset[start : start + length]

            data = [
                {
                    "id": posyandu.id,
                    "name": posyandu.name,
                    "address": posyandu.address,
                    "village": posyandu.village.name,
                }
                for posyandu in queryset
            ]

            return JsonResponse(
                {
                    "draw": draw,
                    "recordsTotal": total_records,
                    "recordsFiltered": total_records,
                    "data": data,
                }
            )

        return super().get(request, *args, **kwargs)


class PosyanduCreateView(CreateView):
    model = Posyandu
    fields = ["name", "address", "village"]  # Include relevant fields
    template_name = "posyandu/posyandu_create_form.html"  # Path to the form template
    success_url = reverse_lazy("posyandu_list")

    def form_valid(self, form):
        messages.success(self.request, "Posyandu berhasil ditambahkan.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Terjadi kesalahan saat menambahkan Posyandu.")
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update(
                {"class": "form-control selectpicker", "data-live-search": "true"}
            )
        return form


class PosyanduUpdateView(UpdateView):
    model = Posyandu
    fields = ["name", "address", "village"]  # Exclude 'parents' field
    template_name = "posyandu/posyandu_update_form.html"
    success_url = reverse_lazy("posyandu_list")

    def form_valid(self, form):
        messages.success(self.request, "Posyandu berhasil diperbarui.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Terjadi kesalahan saat memperbarui Posyandu.")
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update(
                {"class": "form-control selectpicker", "data-live-search": "true"}
            )
        return form


class PosyanduDeleteView(DeleteView):
    model = Posyandu
    template_name = "posyandu/posyandu_confirm_delete.html"
    success_url = reverse_lazy("posyandu_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Posyandu berhasil dihapus.")
        return super().delete(request, *args, **kwargs)
