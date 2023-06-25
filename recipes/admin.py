from django.db.models import F
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum, Max
from .models import Recipe
import json
from django import forms
from django.contrib.admin import widgets
from django.utils.html import format_html


class RecipeForm(forms.ModelForm):
    new_posted_date = forms.DateField(required=False, widget=widgets.AdminDateWidget)

    class Meta:
        model = Recipe
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        new_posted_date = cleaned_data.get("new_posted_date")

        # If a new_posted_date is provided, update the posted_date field
        if new_posted_date:
            cleaned_data["posted_date"] = new_posted_date

        return cleaned_data


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
    list_display = (
        "title",
        "meal_type",
        "cuisine_types",
        "recipe_difficulty",
        "calories",
        "instructions",
        "ingredients",
        "image",
        "rating",
        "preptime_hours",
        "preptime_minutes",
        "servings",
        "cooktime_hours",
        "cooktime_minutes",
        "price",
        "posted_date",
        "total_preptime",
        "total_cooktime",
    )
    list_filter = ("meal_type", "recipe_difficulty")
    change_list_template = 'admin/recipes/change_list.html'  # Path to your custom change_list.html template

    def changelist_view(self, request, extra_context=None):
        # Retrieve the name of the administrator
        admin_name = User.objects.get(username=request.user.username).get_full_name()
        recipe_count = Recipe.objects.count()
        user_count = User.objects.count()
        recipe_preptime = Recipe.objects.values("title").annotate(total_preptime=F("total_preptime"))
        recipe_cooktime = Recipe.objects.values("title").annotate(total_cooktime=F("total_cooktime"))
        recipe_prices = Recipe.objects.values("title", "price")
        recipe_ratings = Recipe.objects.values("title", "rating").annotate(count=Count("id"))
        recipe_with_highest_rating = Recipe.objects.order_by("-rating").first()
        cuisine_type_counts = Recipe.objects.values("cuisine_types").annotate(count=Count("id"))

        # Retrieve the count of recipes per meal type
        meal_type_counts = Recipe.objects.values("meal_type").annotate(count=Count("id"))
        serving_data = Recipe.objects.values("title").annotate(servings=Sum("servings"))
        recipe_difficulties = Recipe.objects.values("recipe_difficulty").annotate(count=Count("id"))

        # Retrieve the count of recipes per month
        recipe_per_month = (
            Recipe.objects.annotate(month=TruncMonth("posted_date"))
            .values("month")
            .annotate(count=Count("id"))
        )

        # Convert the querysets to JSON format and format the month
        recipe_per_month_formatted = []
        for entry in recipe_per_month:
            month = entry["month"].strftime("%B %Y")  # Format the month as "Month Year"
            count = entry["count"]
            recipe_per_month_formatted.append({"month": month, "count": count})

        recipe_per_month_as_json = json.dumps(recipe_per_month_formatted, cls=DjangoJSONEncoder)

        # Convert the querysets to JSON format
        meal_type_counts_as_json = json.dumps(list(meal_type_counts), cls=DjangoJSONEncoder)
        serving_data_as_json = json.dumps(list(serving_data), cls=DjangoJSONEncoder)
        recipe_difficulties_as_json = json.dumps(list(recipe_difficulties), cls=DjangoJSONEncoder)
        recipe_preptime_as_json = json.dumps(list(recipe_preptime), cls=DjangoJSONEncoder)
        recipe_cooktime_as_json = json.dumps(list(recipe_cooktime), cls=DjangoJSONEncoder)
        recipe_prices_as_json = json.dumps(list(recipe_prices), cls=DjangoJSONEncoder)
        recipe_ratings_as_json = json.dumps(list(recipe_ratings), cls=DjangoJSONEncoder)
        cuisine_type_counts_as_json = json.dumps(list(cuisine_type_counts), cls=DjangoJSONEncoder)

        extra_context = extra_context or {
            "meal_type_counts": meal_type_counts_as_json,
            "serving_data": serving_data_as_json,
            "recipe_difficulties": recipe_difficulties_as_json,
            "admin_name": admin_name,
            "recipe_per_month": recipe_per_month_as_json,
            "user_count": user_count,
            "recipe_count": recipe_count,
            "recipe_preptime": recipe_preptime_as_json,
            "recipe_cooktime": recipe_cooktime_as_json,
            "recipe_prices": recipe_prices_as_json,
            "recipe_ratings": recipe_ratings_as_json,
            "recipe_with_highest_rating": recipe_with_highest_rating,
            "cuisine_type_counts": cuisine_type_counts_as_json,

        }

        # THIS IS FOR THE MAX PREPTIME COOKTIME AND PRICE
        max_preptime_recipe = max(recipe_preptime, key=lambda x: x["total_preptime"])
        max_cooktime_recipe = max(recipe_cooktime, key=lambda x: x["total_cooktime"])
        max_price_recipe = max(recipe_prices, key=lambda x: x["price"])

        # Add the recipe with the highest total preptime to the template context
        extra_context["max_preptime_recipe"] = max_preptime_recipe
        extra_context["max_cooktime_recipe"] = max_cooktime_recipe
        extra_context["max_price_recipe"] = max_price_recipe

        # THIS IS FOR THE IMAGES OF THE MAX------
        recipe_with_max_preptime = Recipe.objects.order_by("-total_preptime").first()
        recipe_with_max_preptime_image_url = recipe_with_max_preptime.image.url if recipe_with_max_preptime else None
        recipe_with_max_cooktime = Recipe.objects.order_by("-total_cooktime").first()
        recipe_with_max_cooktime_image_url = recipe_with_max_cooktime.image.url if recipe_with_max_cooktime else None
        recipe_with_max_price = Recipe.objects.order_by("-price").first()
        recipe_with_max_price_image_url = recipe_with_max_price.image.url if recipe_with_max_price else None

        extra_context["recipe_with_max_cooktime_image_url"] = recipe_with_max_cooktime_image_url
        extra_context["recipe_with_max_preptime_image_url"] = recipe_with_max_preptime_image_url
        extra_context["recipe_with_max_price_image_url"] = recipe_with_max_price_image_url

        return super().changelist_view(request, extra_context=extra_context)