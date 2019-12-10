from django.contrib import admin

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from fediverse import models

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "display_name",
        "is_bot",
        "is_manualFollow",
        "is_suspended",
        "is_staff",
        "registered",
        "updated"
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
                "is_manualFollow",
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
    search_fields = ["username", "display_name"]
    list_filter = ["registered", "updated", "is_staff", "is_suspended"]

    def get_queryset(self, request):
        sqs = super().get_queryset(request)
        return sqs.filter(is_active=True)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            only = ["username", "is_superuser"]
            if obj.is_staff == False:
                only.append("groups")
                only.append("user_permissions")
            if obj.is_superuser:
                only.append("is_suspended")
            return only
        else:
            return ["is_superuser", "is_suspended", "groups", "user_permissions"]
        
    def delete_model(self, request, obj):
        obj.is_active = False
        obj.save()

    def has_delete_permission(self, request, obj=None):
        if obj != None:
            if obj.is_superuser:
                return False
            else:
                return not request.user == obj
        else:
            return True

class PostAdmin(admin.ModelAdmin):
    list_display = ("uuid", "parent", "parentFedi", "posted")
    search_fields = ("uuid", "body")
    list_filter = (
        "posted", 
        ("parent", RelatedDropdownFilter),
        ("parentFedi", RelatedDropdownFilter)
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

def make_suspend(modeladmin, request, queryset):
    queryset.update(is_suspended=True)
make_suspend.short_description = "選択したユーザーを凍結"

def destroy_suspend(modeladmin, request, queryset):
    queryset.update(is_suspended=False)
destroy_suspend.short_description = "選択したユーザーを凍結解除"

class FediverseUserAdmin(admin.ModelAdmin):
    list_display = ("__str__", "display_name", "is_bot", "is_suspended")
    list_filter = (
        "Host",
        "is_bot",
        "is_suspended"
    )
    search_fields = ("username", "display_name", "Host", "description")
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
                "is_bot",
                "is_manualFollow",
                "is_suspended"
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
    actions = [make_suspend, destroy_suspend]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.FediverseUser, FediverseUserAdmin)
admin.site.register(models.BlackDomain)
