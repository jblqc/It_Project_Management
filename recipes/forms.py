from django import forms
from djrichtextfield.widgets import RichTextWidget
from .models import Recipe


class RecipeForm(forms.ModelForm):
    """Form to create a recipe"""

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "ingredients",
            "instructions",
            "image",
            "image_alt",
            "meal_type",
            "recipe_difficulty",
            "cuisine_types",
            "calories",
            "preptime_hours",
            "preptime_minutes",
            "servings",
            "cooktime_hours",
            "cooktime_minutes",
            "price",

        ]

        ingredients = forms.CharField(widget=RichTextWidget())
        instructions = forms.CharField(widget=RichTextWidget())

        widget = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }

        labels = {
            "title": "Recipe Title",
            "description": "Description",
            "ingredients": "Recipe Ingredients",
            "instructions": "Recipe Instructions",
            "image": "Recipe Image",
            "image_alt": "Describe Image",
            "meal_type": "Meal Type",
            "recipe_difficulty": "Recipe Difficulty",
            "cuisine_types": "Cuisine Type",
            "calories": "Calories",
            "preptime_hours": "Preparation Time (HR)",
            "preptime_minutes": "Preparation Time (MINUTES)",
            "cooktime_hours": "Cooking Time (HR)",
            "cooktime_minutes": "Cooking Time (MINUTES)",
            "servings": "Servings",
            "price": "Estimated Cost (PHP)",
        }


class RatingForm(forms.Form):
    RATING_CHOICES = [
        (1, "1 star"),
        (2, "2 stars"),
        (3, "3 stars"),
        (4, "4 stars"),
        (5, "5 stars"),
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)


