from django.contrib import admin

from fediverse import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Post)
admin.site.register(models.FediverseUser)
