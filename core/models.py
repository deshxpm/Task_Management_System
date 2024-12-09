from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import *

class User(AbstractUser):
    # Add custom fields if needed
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.username

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
    is_deleted = models.BooleanField(default=False)  # Soft delete support
    is_read = models.BooleanField(default=False)  # Soft delete support

    def __str__(self):
        return f"Message from {self.sender.username} on {self.task.title}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"
