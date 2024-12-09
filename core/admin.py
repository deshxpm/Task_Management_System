from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, Task, ChatMessage, Notification

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'profile_picture')}),
    )


admin.site.register(Task)
admin.site.register(ChatMessage)
admin.site.register(Notification)