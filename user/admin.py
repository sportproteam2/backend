from django.contrib import admin
from .models import *



admin.site.register(User)
admin.site.register(Role)
admin.site.register(Trainer)
admin.site.register(Admin)
admin.site.register(Editor)
