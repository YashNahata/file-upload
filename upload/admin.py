from django.contrib import admin
from .models import File, Bin

# Register your models here.
admin.site.register((File, Bin))
