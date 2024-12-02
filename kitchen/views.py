from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView

from kitchen.models import DishType, Dish, Cook


@login_required
def index(request):
    total_types = DishType.objects.count()
    total_dishes = Dish.objects.count()
    total_cooks = Cook.objects.count()
    context = {
        "total_types": total_types,
        "total_dishes": total_dishes,
        "total_cooks": total_cooks
    }
    render(request, index.html, context)


class DishListView(ListView):
    model = Dish
    paginate_by = 5

    def get_queryset(self):
        return (Dish.objects.select_related("dish_type")
                .prefetch_related("cookers")
                .order_by("name"))