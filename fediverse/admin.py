from django.contrib import admin

from fediverse import models

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'display_name', 'is_bot', 'is_suspended', 'is_active', 'registered', 'updated')
    fieldsets = [
        ("基本情報", {
            "fields": [
                "username",
                "display_name",
                "description"
            ]
        }),
        ("アカウント状態", {
            "fields": [
                "is_bot",
                "is_active",
                "is_suspended",
                "is_staff",
                "is_superuser"
            ]
        }),
        ("管理サイト権限", {
            "fields": [
                "groups",
                "user_permissions"
            ]
        })
    ]
    search_fields = ['username', 'display_name']
    list_filter = ['registered', 'updated']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["username", "is_superuser"]
        else:
            return ["is_superuser"]

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Post)
admin.site.register(models.FediverseUser)
