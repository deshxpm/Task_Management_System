from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, Task, ChatMessage, Notification, Company, Department, Designation

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'profile_picture', 'company', 'role')}),
    )


admin.site.register(Task)
admin.site.register(ChatMessage)
admin.site.register(Notification)
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Designation)