from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from recipes.models import Recipe
#allow us to load a template

class Index(ListView):
    template_name = 'home/index.html'
    model = Recipe
    context_object_name = 'recipes'

    def get_queryset(self):
        return self.model.objects.all()[:3]
