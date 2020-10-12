from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, Item, GroupOfUsers, User, Location


admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(GroupOfUsers)
admin.site.register(User, UserAdmin)
admin.site.register(Location)
