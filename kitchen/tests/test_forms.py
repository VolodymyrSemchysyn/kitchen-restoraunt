from django.test import TestCase
from kitchen.forms import DishNameSearchForm, DishForm
from kitchen.models import Ingredient


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


class TestDishForm(TestCase):
    def setUp(self):
        self.ingredient1 = Ingredient.objects.create(name="Salt")
        self.ingredient2 = Ingredient.objects.create(name="Pepper")
        self.valid_data = {
            "name": "Spaghetti",
            "description": "Delicious spaghetti with tomato sauce.",
            "price": 12.5,
            "dish_type": "Main Course",
            "ingredients": [self.ingredient1.id, self.ingredient2.id],
            "cooks": [],
        }

    def test_valid_dish_form(self):
        form = DishForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_negative_price(self):
        invalid_data = self.valid_data.copy()
        invalid_data["price"] = -5
        form = DishForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Price cannot be negative.", form.errors["price"])

    def test_missing_required_fields(self):
        invalid_data = self.valid_data.copy()
        del invalid_data["name"]
        form = DishForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
