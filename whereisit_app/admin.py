from django.contrib import admin
from .models import Profile, Item, GroupOfUsers, User, Location


admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(GroupOfUsers)
admin.site.register(User)
admin.site.register(Location)
