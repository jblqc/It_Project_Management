from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.db.models import Count


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "bio", "image")  # Include the 'bio' field in the list_display
    change_list_template = 'admin/profiles/change_list.html'  # Path to your custom change_list.html template


    def changelist_view(self, request, extra_context=None):
        # Retrieve the name of the administrator
        admin_name = User.objects.get(username=request.user.username).get_full_name()
        top_user = User.objects.annotate(num_recipes=Count('recipe_owner')).order_by('-num_recipes').first()

        if top_user:
            # Retrieve the profile of the user with the most number of recipes
            top_profile = Profile.objects.get(user=top_user)
            avatar = top_profile.image.url
            num_recipes = top_user.num_recipes
        else:
            avatar = None
            num_recipes = None
        
        users = User.objects.all()

        extra_context = extra_context or {
            "admin_name": admin_name,
            "top_user": top_user,
            "avatar": avatar,
            "num_recipes": num_recipes,
            "users": users,
        }
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Profile, ProfileAdmin)
