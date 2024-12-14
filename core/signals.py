from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail

# @receiver(post_save, sender=Task)
# def task_assignment_notification(sender, instance, created, **kwargs):
#     if created:
#         message = f"You have been assigned a new task: {instance.title}"
#         Notification.objects.create(user=instance.assigned_to, message=message)

#         # Send the notification via WebSocket
#         channel_layer = get_channel_layer()
#         group_name = f"user_{instance.assigned_to.id}"

#         async_to_sync(channel_layer.group_send)(
#             group_name,
#             {
#                 'type': 'send_notification',
#                 'message': message
#             }
#         )


@receiver(post_save, sender=Task)
def notify_task_updates(sender, instance, created, **kwargs):
    print("Signal RUN")
    if created:
        print("Obj created")
        # Task created: Notify the assignee
        if instance.assigned_to:
            print("instance founded")
            message=f'A new task "{instance.title}" has been assigned to you.'
            # Create a database notification
            Notification.objects.create(
                user=instance.assigned_to,
                message=message
            )

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


            # Send email notification
            try:
                send_mail(
                    subject='New Task Assigned',
                    message=message,
                    from_email='noreply@yourdomain.com',
                    recipient_list=[instance.assigned_to.email],
                )
            except Exception as e:
                print(e)
    else:
        # Task updated: Notify both assigner and assignee
        notifications = []
        if instance.user:
            notifications.append(
                Notification(
                    user=instance.user,
                    message=f'The task "{instance.title}" status has been updated to "{instance.status}".'
                )
            )

        if instance.assigned_to and instance.assigned_to != instance.user:
            notifications.append(
                Notification(
                    user=instance.assigned_to,
                    message=f'The task "{instance.title}" status has been updated to "{instance.status}".'
                )
            )

        # Bulk create notifications
        Notification.objects.bulk_create(notifications)

        # Send email notifications
        recipients = [instance.user.email]
        if instance.assigned_to and instance.assigned_to.email not in recipients:
            recipients.append(instance.assigned_to.email)

        try:
            send_mail(
                subject='Task Status Updated',
                message=f'The task "{instance.title}" status has been updated to "{instance.status}".',
                from_email='noreply@yourdomain.com',
                recipient_list=recipients,
            )
        except Exception as e:
            print(e)
