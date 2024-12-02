from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from kitchen.forms import DishNameSearchForm
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
        queryset = Dish.objects.select_related("dish_type").prefetch_related("cookers").order_by("name")
        form = DishNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset

