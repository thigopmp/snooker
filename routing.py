from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from myapp import consumers

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/atualizar_placar/', consumers.AtualizarPlacarConsumer.as_asgi()),
        ])
    ),
})
