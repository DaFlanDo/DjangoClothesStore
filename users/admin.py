from django.contrib import admin

from products.admin import BasketsAdmin
from users.models import User,EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'last_name',  'is_staff', 'date_joined',)
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    search_fields = ('id', 'username', 'email', 'first_name', 'last_name')
    ordering = ('id',)
    inlines = [BasketsAdmin]


@admin.register(EmailVerification)
class UserEmailVerification(admin.ModelAdmin):
    list_display = ('user','code','expiration',)
    fields = ('user','code','expiration','on_created',)
    readonly_fields = ('on_created',)
# Register your models here.
