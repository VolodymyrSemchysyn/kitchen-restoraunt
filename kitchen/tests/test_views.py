from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.tests import COOK_LIST_URL
from kitchen.models import DishType, Ingredient, Dish

INDEX_URL = reverse("kitchen:index")
DISH_LIST_URL = reverse("kitchen:dish-list")


class PublicDishViewTest(TestCase):
    def test_login_required(self) -> None:
        result_index = self.client.get(INDEX_URL)
        result_dish = self.client.get(DISH_LIST_URL)
        cook_list = self.client.get(COOK_LIST_URL)
        self.assertNotEqual(result_index.status_code, 200)
        self.assertNotEqual(result_dish.status_code, 200)
        self.assertNotEqual(cook_list.status_code, 200)


class PrivateDishViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="chef_anna", password="testpassword123"
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(name="Main Course")
        self.ingredient = Ingredient.objects.create(name="Garlic")
        self.cook = get_user_model().objects.create_user(
            username="chef_anna",
            password="testpassword123",
            first_name="Anna",
            last_name="Smith",
            years_of_experience=5,
        )
        self.dish = Dish.objects.create(
            name="Grilled Chicken",
            price=100.0,
            dish_type=self.dish_type,
            description="A delicious grilled chicken with garlic",
        )
        self.dish.ingredients.add(self.ingredient)
        self.dish.cooks.add(self.cook)

    def test_retrieve_dish_list(self) -> None:
        response = self.client.get(DISH_LIST_URL)
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dishes),
        )
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_update_dish_manual_logic(self) -> None:
        data = {
            "name": "Updated Chicken",
            "price": 120.0,
            "dish_type": self.dish_type.id,
            "description": "Updated description",
            "ingredients": [self.ingredient.id],
            "cooks": [self.cook.id],
        }
        response = self.client.post(
            reverse("kitchen:dish-update", args=[self.dish.id]), data
        )
        self.assertEqual(response.status_code, 302)
        updated_dish = Dish.objects.get(id=self.dish.id)
        self.assertEqual(updated_dish.name, "Updated Chicken")
        self.assertEqual(updated_dish.price, 120.0)

    def test_delete_dish_manual_logic(self) -> None:
        previous_count = Dish.objects.count()
        response = self.client.post(reverse("kitchen:dish-delete", args=[self.dish.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Dish.objects.count(), previous_count - 1)
