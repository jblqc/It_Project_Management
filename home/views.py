from django.views.generic import TemplateView #allow us to load a template

class Index(TemplateView):
    template_name = 'home/index.html'
