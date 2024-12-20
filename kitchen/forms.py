from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Dish, Ingredient, Cook


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

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    years_of_experience = forms.IntegerField(required=True)

    class Meta:
        model = Cook
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "years_of_experience"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["years_of_experience"].widget.attrs["class"] = "form-control"

    def clean_years_of_experience(self):
        years_of_experience = self.cleaned_data.get("years_of_experience")
        if years_of_experience < 0:
            raise forms.ValidationError("Years of experience cannot be negative.")
        return years_of_experience
