from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from kitchen.forms import DishNameSearchForm
from kitchen.models import DishType, Dish, Cook, DishIngredient


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
    return render(request, "kitchen/index.html", context)


class DishListView(LoginRequiredMixin,ListView):
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type").prefetch_related("cooks").order_by("name")
        form = DishNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset

class DishDetailView(LoginRequiredMixin, DetailView):
    model = Dish

    def get_queryset(self):
        dish_ingredients = Prefetch("ingredients_in_dish", queryset=DishIngredient.objects.all())

        return Dish.objects.prefetch_related(
            "ingredients",
            "cooks",
            dish_ingredients
        ).select_related(
            "dish_type"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dish = self.get_object()
        dish_ingredients = DishIngredient.objects.filter(dish=dish)
        context["dish_ingredients"] = dish_ingredients
        return context