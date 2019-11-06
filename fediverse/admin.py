from django.contrib import admin

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from fediverse import models

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'display_name',
        'is_bot',
        'is_suspended',
        'is_staff',
        'registered',
        'updated'
    )
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
    list_filter = ['registered', 'updated', 'is_staff', 'is_suspended']

    def get_queryset(self, request):
        sqs = super().get_queryset(request)
        return sqs.filter(is_active=True)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            only = ["username", "is_superuser"]
            if obj.is_active == False:
                only.append("is_active")
            if obj.is_staff == False:
                only.append("groups")
                only.append("user_permissions")
            return only
        else:
            return ["is_superuser", "is_active", "is_suspended", "groups", "user_permissions"]
        
    def delete_model(self, request, obj):
        obj.is_active = False
        obj.save()

class PostAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'parent', 'parentFedi', 'posted')
    search_fields = ('uuid', 'body')
    list_filter = (
        'posted', 
        ('parent', RelatedDropdownFilter),
        ('parentFedi', RelatedDropdownFilter)
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class FediverseUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'display_name', 'is_bot')
    search_fields = ('username', 'display_name', 'Host', 'description')
    fieldsets = [
        ("基本情報", {
            "fields": [
                "username",
                "display_name",
                "Host",
                "description"
            ]
        }),
        ("アカウント状態", {
            "fields": [
                "is_bot"
            ]
        }),
        ("URL", {
            "fields": [
                "Inbox",
                "Outbox",
                "SharedInbox",
                "Featured",
                "Followers",
                "Following",
                "Uri",
                "Url"
            ]
        })
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.FediverseUser, FediverseUserAdmin)
admin.site.register(models.BlackDomain)
