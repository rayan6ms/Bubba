from django.contrib import admin
from .models import User
# Register your models here.

admin.site.register(User)


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("username", "password")