import json
from channels.layers import get_channel_layer
from asgiref.testing import ApplicationCommunicator

from .consumers import ChartConsumer


async def send_realtime_data(data):
    channel_layer = get_channel_layer()
    communicator = ApplicationCommunicator(
        ChartConsumer.as_asgi(), {"type": "websocket.connect"}
    )
    connected, _ = communicator.connect()
    assert connected

    await communicator.send_json_to({"type": "receive", "text": json.dumps(data)})
