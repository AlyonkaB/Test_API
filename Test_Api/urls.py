"""
URL configuration for Test_Api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from Test_Api import settings

urlpatterns = [
    # Admin:
    path("admin/", admin.site.urls),
    # Toolbar:
    path("__debug__/", include("debug_toolbar.urls")),
    # YOUR PATTERNS
    path("api/station/", include("db.urls", namespace="db")),
    path("api/user/", include("user.urls", namespace="user")),
    # Optional drf-spectacular:
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI(Swagger):
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Optional UI(Redoc)
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
