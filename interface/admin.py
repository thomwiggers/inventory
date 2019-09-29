from django.contrib import admin

from interface import models

admin.site.register(models.Brand)
admin.site.register(models.Product)
admin.site.register(models.Packaging)
