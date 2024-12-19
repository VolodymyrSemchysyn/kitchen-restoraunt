from unittest import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

COOK_LIST_URL = reverse("accounts:cook-list")


def test_cook_str(self) -> None:
    cook = self.cook
    self.assertEqual(
        str(cook),
        f"{cook.username} "
        f"({cook.first_name} "
        f"{cook.last_name} "
        f"{cook.years_of_experience})",
    )


class PrivateCookViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="chef_anna",
            password="testpassword123",
            first_name="Anna",
            last_name="Smith",
        )
        self.client.force_login(self.user)

    def test_retrieve_cook_list(self) -> None:
        response = self.client.get(COOK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cooks = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["cook_list"]),
            list(cooks),
        )
        self.assertTemplateUsed(response, "accounts/cook_list.html")

    def test_register_new_cook_manual_logic(self) -> None:
        previous_count = get_user_model().objects.count()
        data = {
            "username": "chef_petro",
            "password1": "securepassword123",
            "password2": "securepassword123",
            "first_name": "Petro",
            "last_name": "MC",
            "email": "petro.@gmail.com",
            "years_of_experience": 3,
        }
        response = self.client.post(reverse("kitchen:register"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), previous_count + 1)
        created_cook = get_user_model().objects.get(username="chef_petro")
        self.assertEqual(created_cook.first_name, "Petro")
        self.assertEqual(created_cook.years_of_experience, 3)

    def test_cook_list_pagination(self) -> None:
        for i in range(6):
            get_user_model().objects.create_user(
                username=f"chef_{i}",
                password="testpassword123",
                first_name=f"FirstName_{i}",
                last_name=f"LastName_{i}",
                years_of_experience=i,
            )
        response = self.client.get(COOK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["cook_list"]), 5)
        self.assertTrue(response.context["is_paginated"])
