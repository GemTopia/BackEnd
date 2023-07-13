from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from users.models import User, SocialMedia


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('user_name', 'email', 'avatar', 'total_gemyto', 'is_admin')
    list_filter = ('is_admin',)
    readonly_fields = ('last_login', 'total_gemyto')

    fieldsets = (
        ('Main', {'fields': ('user_name', 'email', 'password', 'avatar', 'total_gemyto')}),
        ('Permissions',
         {'fields': ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('user_name', 'email', 'password')}),
    )

    search_fields = ('user_name', 'email')
    ordering = ('created_at',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


admin.site.register(User, UserAdmin)
<<<<<<< HEAD
admin.site.register(SocialMedia)
=======
>>>>>>> main
