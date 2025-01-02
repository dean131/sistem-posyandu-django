from django.views.generic.list import ListView
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from .models import Child


class ChildListView(ListView):
    model = Child
    template_name = "child/child_list.html"
    context_object_name = "children"

    def get_queryset(self):
        # Add optional filtering or ordering logic here
        query = self.request.GET.get("q", "").strip()
        queryset = Child.objects.all().order_by("-created_at")
        if query:
            queryset = queryset.filter(full_name__icontains=query)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            page = self.request.GET.get("page", 1)
            per_page = self.request.GET.get("length", 10)
            search = self.request.GET.get("search[value]", "")

            queryset = self.get_queryset()
            if search:
                queryset = queryset.filter(full_name__icontains=search)

            paginator = Paginator(queryset, per_page)
            children_page = paginator.get_page(page)

            data = [
                {
                    "id": child.id,
                    "full_name": child.full_name,
                    "gender": child.get_gender_display(),
                    "birth_date": child.birth_date.strftime("%d-%m-%Y"),
                    "parent_name": child.parent.full_name,
                }
                for child in children_page
            ]

            return JsonResponse(
                {
                    "data": data,
                    "recordsTotal": queryset.count(),
                    "recordsFiltered": queryset.count(),
                }
            )
        return super().render_to_response(context, **response_kwargs)


class ChildDetailView(DetailView):
    model = Child
    template_name = "child/child_detail.html"
    context_object_name = "child"

    def get_object(self):
        # Retrieve the child object based on the ID from the URL
        return get_object_or_404(Child, pk=self.kwargs["pk"])
