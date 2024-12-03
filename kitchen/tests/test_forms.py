from django.test import TestCase
from kitchen.forms import DishNameSearchForm


class TestDishSearchForm(TestCase):
    def test_dish_name_search_form(self) -> None:
        form = DishNameSearchForm(data={"name": "Grilled Chicken"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Grilled Chicken")

    def test_dish_type_search_form(self) -> None:
        form = DishNameSearchForm(data={"dish_type": "Main Course"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["dish_type"], "Main Course")

    def test_dish_include_ingredients_search_form(self) -> None:
        form = DishNameSearchForm(data={"include_ingredients": True})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["include_ingredients"], True)