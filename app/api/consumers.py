import json
from channels.generic.websocket import AsyncWebsocketConsumer
from IoTAppBackEnd.KasaSmartPowerStrip import SmartPowerStrip
from api.models import chat_room_data
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

class StripConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.power_strip = SmartPowerStrip("60.198.44.134")
            # self.home_name = self.scope["url_route"]["kwargs"]["home_name"]
            # self.home_group_name = "chat_%s" % self.home_name

            # # # # # Join room group
            # await self.channel_layer.group_add(self.home_group_name, self.channel_name)
            await self.accept()

    # async def disconnect(self, close_code):
    #     # Leave room group
    #     if self.scope["user"].is_anonymous:
    #         await self.close()
    #     else:
    #         await self.channel_layer.group_discard(
    #             self.home_group_name, self.channel_name
    #         )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        status = list(message.split(":"))
        print(status)
        self.power_strip.toggle_plug(status[0], plug_num=int(status[1]))

        # # Send message to room group
        # await self.channel_layer.group_send(self.room_group_name, {
        #     'type': 'chat_message',
        #     'message': message
        # })

    # # Receive message from room group
    # async def chat_message(self, event):
    #     message = event['message']

    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({'message': message}))


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user_name = self.scope["url_route"]["kwargs"]["user_name"]
            self.home_group_name = "chat_%s" % self.user_name

            # # # # # Join room group
            await self.channel_layer.group_add(self.home_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_discard(
                self.home_group_name, self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.home_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)


        await self.accept()
       

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

      
        # save message to database
        await self.save_message(message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
    
    @sync_to_async
    def save_message(self, message):
        chat_room_data.objects.create(chat_room_name=self.room_name, message=message)