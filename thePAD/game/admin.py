from django.contrib import admin

from .models import User, Action

class ActionInline(admin.StackedInline) :
    model = Action
    extra = 1

class UserAdmin(admin.ModelAdmin) :
    fields = ['name']
    inlines = [ActionInline]

class ActionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields' : ['user']}),
        ('Information date', {'fields' : ['act_date']}),
        ('Valeurs',          {'fields' : ['point']})
    ]

admin.site.register(User, UserAdmin)
admin.site.register(Action, ActionAdmin)