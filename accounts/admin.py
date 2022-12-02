from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PersistentId


class PersistentIdInline(admin.TabularInline):
    model = PersistentId
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ["date_joined", "last_login"]
    list_display = ["username", "email", "is_active", "is_staff", "is_superuser"]
    list_editable = ["is_active", "is_staff", "is_superuser"]
    inlines = [PersistentIdInline, ]
    fieldsets = (
        (None, {"fields": (("username", "is_active", "is_staff", "is_superuser",),
                           "password",
                           "origin",
                           )
                }),

        ("Registration", {"fields": (("first_name", "last_name"),
                                     "email",
                                     ("taxpayer_id",),
                                     ("gender", "place_of_birth", "birth_date",)
                                     )
                          }),

        ("Permissions", {"fields": ("groups", "user_permissions"),
                         "classes": ("collapse",)
                         }),

        ("Access system date", {"fields": ("date_joined", "last_login",)
                                }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(PersistentId)
class PersistentIdAdmin(admin.ModelAdmin):
    list_display = ['user', 'persistent_id', 'recipient_id', 'created']
    list_filter = ('created',)


admin.site.site_header = "AUTHENTICATION GATE"
admin.site.site_title = "NATHOS IT"