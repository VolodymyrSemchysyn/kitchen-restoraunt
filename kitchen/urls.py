from django.urls import path

from kitchen import views
from kitchen.views import DishListView

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "dishes/",
        DishListView.as_view(),
        name="dish-list"
    ),

]

app_name = "kitchen"