from django.contrib import admin

from products.admin import BasketsAdmin
from users.models import User,EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'date_joined','is_verification',)

    def is_verification_display(self, obj):
        return obj.is_verification

    is_verification_display.short_description = ('Is Verified')
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
