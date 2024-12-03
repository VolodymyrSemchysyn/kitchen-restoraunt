from django import forms
from .models import Dish, Ingredient


class DishNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class DishForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Dish
        fields = ["name", "description", "price", "dish_type", "ingredients", "cooks"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter dish name"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter dish description"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter price"
            }),
            "dish_type": forms.Select(attrs={
                "class": "form-control"
            }),
            "cooks": forms.SelectMultiple(attrs={
                "class": "form-control"
            }),
        }
        labels = {
            "name": "Dish Name",
            "description": "Description",
            "price": "Price (UA)",
            "dish_type": "Dish Type",
            "ingredients": "Ingredients",
            "cooks": "Assigned Cooks",
        }
