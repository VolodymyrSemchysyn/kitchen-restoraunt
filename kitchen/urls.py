from django.urls import path

from kitchen import views
from kitchen.views import DishListView, DishDetailView

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "dishes/",
        DishListView.as_view(),
        name="dish-list"
    ),
    path(
        "dishes/<int:pk>/",
        DishDetailView.as_view(),
        name="dish-detail"
    ),

]

app_name = "kitchen"