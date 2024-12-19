from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from kitchen.forms import DishNameSearchForm, DishForm
from kitchen.models import DishType, Dish, Cook


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "kitchen/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "total_types": DishType.objects.count(),
                "total_dishes": Dish.objects.count(),
                "total_cooks": Cook.objects.count(),
            }
        )
        return context


class DishListView(LoginRequiredMixin, ListView):
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = (
            Dish.objects.select_related("dish_type")
            .prefetch_related("cooks")
            .order_by("name")
        )
        form = DishNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class DishDetailView(LoginRequiredMixin, DetailView):
    queryset = Dish.objects.prefetch_related("ingredients", "cooks").select_related(
        "dish_type"
    )
    model = Dish

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dish = self.get_object()

        dish_ingredients = dish.ingredients.all()

        context["dish_ingredients"] = dish_ingredients
        return context


class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    success_url = "/dishes/"


class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")
