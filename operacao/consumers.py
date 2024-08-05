import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PlacarConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.mesa_id = self.scope['url_route']['kwargs']['mesa_id']
        self.mesa_group_name = f'placar_{self.mesa_id}'

        await self.channel_layer.group_add(
            self.mesa_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.mesa_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        if action == 'update_placar':
            await self.channel_layer.group_send(
                self.mesa_group_name,
                {
                    'type': 'placar_update',
                    'message': data
                }
            )

    async def placar_update(self, event):
        message = event['message']

        await self.send(text_data=json.dumps(message))
