from django.contrib import admin

from .models import User, Action

admin.site.register(User)
admin.site.register(Action)