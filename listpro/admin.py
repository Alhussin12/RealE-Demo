from atexit import register
from django.contrib import admin
from .models import proerities ,proeritie
# Register your models here.

admin.site.register(proerities)
admin.site.register(proeritie)
