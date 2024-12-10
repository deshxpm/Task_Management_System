from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import *

class User(AbstractUser):
    # Add custom fields if needed
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name="role_of_user",null=True,blank=True)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name="users")

    def __str__(self):
        return self.username
    
    def mask_phone_number(self):
        """
        Masks the phone number, showing only the last 4 digits.
        Example: *****6789
        """
        if self.phone_number and len(self.phone_number) > 4:
            return f"{'*' * (len(self.phone_number) - 4)}{self.phone_number[-4:]}"
        return self.phone_number  # Return as is if not enough digits

    def mask_email(self):
        """
        Masks the email, hiding part of the local part before the '@'.
        Example: j******e@gmail.com
        """
        if self.email:
            local, domain = self.email.split('@')
            if len(local) > 2:
                return f"{local[0]}{'*' * (len(local) - 2)}{local[-1]}@{domain}"
            return self.email  # Return as is if local part is too short
        return None  # Return None if email is not provided

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Permission(Base):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Role(Base):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, blank=True)
    company = models.ForeignKey('Company',on_delete=models.CASCADE,null=True, related_name="company_role")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} -> {self.company.name if self.company else '--'}"    

class Company(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company_user", null=True, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=60,null=True, blank=True)
    logo = models.ImageField(upload_to='company_logo/', blank=True, null=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name}"
    
class Address(Base):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="address_company")
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name}"

class Department(Base):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='department_company',null=True,blank=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def _str_(self):
        return f"{self.name}"

class Designation(Base):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='designation_company',null=True,blank=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.name}"

# Task Model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        User, related_name='created_tasks', on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        User, related_name='assigned_tasks', on_delete=models.CASCADE
    )
    parent_task = models.ForeignKey(
        'self', related_name='subtasks', on_delete=models.SET_NULL, blank=True, null=True
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    eta = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Chat Model
class ChatMessage(models.Model):
    task = models.ForeignKey('Task', related_name='task_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(blank=True, null=True)  # Track message edits
    is_deleted = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} on {self.task.title}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"
