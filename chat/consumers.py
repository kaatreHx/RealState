from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import json
from .models import ChatModel
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'].split('_')
        self.user1 = int(self.room_name[0])
        self.user2 = int(self.room_name[1])
            
        # Only allow one of the two users in the room
        if self.scope["user"].id not in [self.user1, self.user2]:
            await self.close()

        #For constant room name
        self.room_name = f"chat_{min(self.user1, self.user2)}_{max(self.user1, self.user2)}"

        # Join room 
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room 
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )   

    # Receive message from WebSocket
    async def receive(self, text_data):
        #Handling Erro
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            sender = self.scope['user']
            sender_id = sender.id 

            receiver_id = 0

            if sender_id == self.user1:
                receiver_id = self.user2
            else:
                receiver_id = self.user1

            #Saving message to database
            await self.save_message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message=message,
                room_name=self.room_name
            )

            # Send message to room 
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender_id,
                    'receiver_id': receiver_id
                }
            )

        except Exception as e:
            print(f"Error in receive: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Failed to process message'
            }))
    
    async def chat_message(self, event):
        #Sending message to client
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id']
        }))
    
    @database_sync_to_async #It is a decorator in django channels. It is used to safely call synchronous Django ORM code from within an asynchronous context as we know our consumer is Async
    def save_message(self, sender_id, receiver_id, message, room_name):
        #Handling Error
        try:
            ChatModel.objects.create(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message=message,
                room_name=room_name
            )
        except Exception as e:
            print(f"Error in save_message: {e}")