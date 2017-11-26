from django.contrib import admin
from .models import User, Resources, UserComment, UserLikes

# Register your models here.
admin.site.register(User)
admin.site.register(Resources)
admin.site.register(UserComment)
admin.site.register(UserLikes)
