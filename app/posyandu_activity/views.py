from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from .models import PosyanduActivity


class PosyanduActivityListView(TemplateView):
    template_name = "posyandu_activity/posyandu_activity_list.html"

    def get(self, request, *args, **kwargs):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            search_value = request.GET.get("search[value]", "").strip()
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_column_name = request.GET.get(f"columns[{order_column_index}][data]")
            order_dir = request.GET.get("order[0][dir]", "asc")

            activities = PosyanduActivity.objects.select_related("posyandu").all()

            # Apply search filter
            if search_value:
                activities = activities.filter(name__icontains=search_value)

            # Apply sorting
            if order_column_name:
                order_column_name = (
                    f"-{order_column_name}"
                    if order_dir == "desc"
                    else order_column_name
                )
                activities = activities.order_by(order_column_name)

            total_records = activities.count()
            activities = activities[start : start + length]

            # Format data for DataTable
            data = [
                {
                    "id": activity.id,
                    "name": activity.name,
                    "description": activity.description,
                    "date": activity.date,
                    "posyandu": activity.posyandu.name,
                }
                for activity in activities
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


class PosyanduActivityDetailView(DetailView):
    model = PosyanduActivity
    template_name = "posyandu_activity/posyandu_activity_detail.html"
    context_object_name = "activity"
