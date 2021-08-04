from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserInfo
from .models import CustomUser, whodonate, Post1

admin.site.register(UserInfo)
admin.site.register(CustomUser)
admin.site.register(whodonate)
admin.site.register(Post1)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)