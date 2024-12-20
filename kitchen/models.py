from django.contrib.auth.models import AbstractUser
from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(null=False, blank=False, default=0)


    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name} {self.years_of_experience})"


class Dish(models.Model):
    name = models.CharField(max_length=55, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="dishes"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        related_name="dishes"
    )
    cooks = models.ManyToManyField(
        Cook,
        blank=False,
        related_name="dishes"
    )

    def __str__(self):
        return f"{self.name}, ({self.dish_type}), {self.cooks}"

