from django.urls import path, include

from accounts.views import RegisterView, CooksListView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path(
        "cooks/",
        CooksListView.as_view(),
        name="cook-list",
    ),
    path("register/", RegisterView.as_view(), name="register"),
]

app_name = "accounts"
