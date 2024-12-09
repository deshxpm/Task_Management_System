import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
# from core.models import ChatMessage, Task

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Import models here to avoid AppRegistryNotReady during startup
        from core.models import ChatMessage, Task
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.room_group_name = f'chat_{self.task_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        from core.models import ChatMessage, Task  # Lazy import
        try:
            data = json.loads(text_data)
            message = data['message']
            file_url = data.get('file')
            sender = self.scope['user']
            
            if not sender.is_authenticated:
                await self.close()  # Close the connection if not authenticated
                return
                
            task = await database_sync_to_async(Task.objects.get)(id=self.task_id)

            # Save message to database
            new_message = await database_sync_to_async(ChatMessage.objects.create)(
                task=task,
                sender=sender,
                message=message,
                file=file_url
            )

            # Send message to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': new_message.id,
                    'sender': sender.username,
                    'message': message,
                    'file': file_url,
                    'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
            )
        except Task.DoesNotExist:
            await self.send(text_data=json.dumps({'error': 'Invalid task ID'}))
        except KeyError as e:
            await self.send(text_data=json.dumps({'error': f'Missing field: {str(e)}'}))
        except Exception as e:
            await self.send(text_data=json.dumps({'error': f'An error occurred: {str(e)}'}))


    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f"user_{self.scope['user'].id}"

        # Join the group for the authenticated user
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        # Send the notification to the WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'task_id': event.get('task_id', None),
            'notification_type': event.get('notification_type', 'general'),
            'timestamp': event.get('timestamp')
        }))
