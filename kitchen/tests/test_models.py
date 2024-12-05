from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import DishType, Ingredient, Dish


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(name="Main Course")
        self.ingredient = Ingredient.objects.create(name="Garlic")
        self.cook = get_user_model().objects.create_user(
            username="chef_anna",
            password="testpassword123",
            first_name="Anna",
            last_name="Smith",
            years_of_experience=5
        )
        self.dish = Dish.objects.create(
            name="Grilled Chicken",
            price=100.0,
            dish_type=self.dish_type,
            description="A delicious grilled chicken with garlic",
        )
        self.dish.ingredients.add(self.ingredient)
        self.dish.cooks.add(self.cook)

    def test_dish_type_str(self) -> None:
        dish_type = self.dish_type
        self.assertEqual(str(dish_type), dish_type.name)

    def test_ingredient_str(self) -> None:
        ingredient = self.ingredient
        self.assertEqual(str(ingredient), ingredient.name)

    def test_cook_str(self) -> None:
        cook = self.cook
        self.assertEqual(
            str(cook),
            f"{cook.username} "
            f"({cook.first_name} "
            f"{cook.last_name} "
            f"{cook.years_of_experience})"
        )

    def test_dish_str(self) -> None:
        dish = self.dish
        self.assertEqual(
            str(dish),
            f"{dish.name}, "
            f"({dish.dish_type}), "
            f"{dish.cooks.all()}"
        )