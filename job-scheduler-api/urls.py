
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django.urls import include, path

schema_view = get_schema_view(
    openapi.Info(
        title="Job Scheduler API",
        default_version="v1",
        description="Job Scheduler API documentation",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=[],
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
   path("api/jobs/", include("apps.scheduler.urls")),
]
