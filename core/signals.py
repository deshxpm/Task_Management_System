from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(post_save, sender=Task)
def task_assignment_notification(sender, instance, created, **kwargs):
    if created:
        message = f"You have been assigned a new task: {instance.title}"
        Notification.objects.create(user=instance.assigned_to, message=message)

        # Send the notification via WebSocket
        channel_layer = get_channel_layer()
        group_name = f"user_{instance.assigned_to.id}"

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                'message': message
            }
        )
