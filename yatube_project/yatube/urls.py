from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("", include("posts.urls", namespace="posts")),
    path("api/", include("api.urls")),
    path("auth/", include("users.urls", namespace="users")),
    path("auth/", include("django.contrib.auth.urls")),
    path("about/", include("about.urls", namespace="about")),
    path("admin/", admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]

handler404 = "core.views.page_not_found"
handler500 = "core.views.server_error"
handler403 = "core.views.permission_denied"
