from django.contrib import admin
from .models import Profile
from django.contrib.admin import widgets
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "bio", "image")
    change_list_template = 'admin/profiles/change_list.html'  # Path to your custom change_list.html template

    def changelist_view(self, request, extra_context=None):
        # Retrieve the name of the administrator
        admin_name = User.objects.get(username=request.user.username).get_full_name()
        extra_context = extra_context or {
            "admin_name": admin_name,
        }
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Profile, ProfileAdmin)
