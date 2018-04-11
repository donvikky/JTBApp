from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from account.models import Profile

class UserProfileInline(admin.TabularInline):
    model = Profile

class MyUserAdmin(UserAdmin):
    inlines = [
        UserProfileInline,
    ]

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)