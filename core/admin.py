from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, Task, ChatMessage, Notification, Company, Department, Designation, Role, Permission

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'profile_picture', 'company', 'role')}),
    )

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_by', 'assigned_to')    

admin.site.register(Task, TaskAdmin)

admin.site.register(ChatMessage)
admin.site.register(Notification)
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Role)
admin.site.register(Permission)