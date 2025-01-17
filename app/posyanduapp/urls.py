"""
URL configuration for posyanduapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include("adminapp.urls")),
    path("", include("account.urls")),
    path("", include("village.urls")),
    path("", include("posyandu.urls")),
    path("", include("posyandu_activity.urls")),
    path("", include("child.urls")),
    path("", include("child_measurement.urls")),
    path("api/", include("account.api.urls")),
    path("api/", include("posyandu.api.urls")),
    path("api/", include("posyandu_activity.api.urls")),
    path("api/", include("village.api.urls")),
    path("api/", include("child.api.urls")),
    path("api/", include("child_measurement.api.urls")),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
