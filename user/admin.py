from django.contrib import admin
from firebase import UserService
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        UserService.create(obj.phone)
        super().save_model(request, obj, form, change)

# admin.site.register(User)
admin.site.register(Role)
admin.site.register(Trainer)
admin.site.register(Admin)
admin.site.register(Editor)
admin.site.register(Region)