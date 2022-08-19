import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .KasaSmartPowerStrip import SmartPowerStrip

class StripConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # if self.scope['user'].is_anonymous:
        #     await self.close()
        # else:
        self.power_strip = SmartPowerStrip("192.168.0.12")
        self.home_name = self.scope['url_route']['kwargs']['home_name']
        self.home_group_name = 'chat_%s' % self.home_name

            # # # # Join room group
        await self.channel_layer.group_add(self.home_group_name,
                                        self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_discard(self.home_group_name,
                                               self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        status = list(message.split(':'))
        print(status[0],int(status[1]))
        self.power_strip.toggle_plug(status[0],plug_num=int(status[1]))

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
