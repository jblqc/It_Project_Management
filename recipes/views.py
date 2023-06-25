from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import(
    CreateView, ListView,
    DetailView, DeleteView,
    UpdateView
    )
from django.contrib.auth.mixins import(
    UserPassesTestMixin, LoginRequiredMixin 
)
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe
from .forms import RecipeForm

from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from .models import Recipe
from .forms import RatingForm
from django.views.generic import TemplateView
from django.views import View
import json

"""""********************************"""

class Recipes(ListView):
    """View all recipes"""

    template_name = "recipes/recipes.html"
    model = Recipe
    context_object_name = "recipes"

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q')
        if query:
            recipes = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(instructions__icontains=query) |
                Q(cuisine_types__icontains=query)
            )
        else:
            recipes = self.model.objects.all()
        return recipes
"""""********************************"""
class RecipeDetail(DetailView):
    """View a single recipe"""

    template_name = "recipes/recipe_detail.html"
    model = Recipe
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RatingForm()
        return context

    def post(self, request, *args, **kwargs):
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = int(form.cleaned_data['rating'])
            recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
            recipe.rating = rating
            recipe.save()
            return render(request, self.template_name, {'object': recipe, 'form': form})
        else:
            return self.get(request, *args, **kwargs)

"""""********************************"""

class AddRecipe(LoginRequiredMixin, CreateView):
    """Add recipe view"""

    template_name = "recipes/add_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddRecipe, self).form_valid(form)
 
"""""********************************"""

class EditRecipe(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    """Edit a recipe"""
    template_name = 'recipes/edit_recipe.html'
    model = Recipe
    form_class = RecipeForm
    success_url = '/recipes/'

    def test_func(self):
        return self.request.user == self.get_object().user
    
"""""********************************"""


class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a recipe"""
    model = Recipe
    success_url = '/recipes/'

    def test_func(self):
        return self.request.user == self.get_object().user
    

@login_required
def rate_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = RatingForm(request.POST)
    if form.is_valid():
        rating = int(form.cleaned_data['rating'])
        recipe.rating = (recipe.rating * recipe.rating_count + rating) / (recipe.rating_count + 1)
        recipe.rating_count += 1
        recipe.save()
    else:
        rating = None
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'form': form, 'rating': rating})


"""*********************"""""

