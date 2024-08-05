from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/placar/(?P<mesa_id>\d+)/$', consumers.PlacarConsumer.as_asgi()),
]
