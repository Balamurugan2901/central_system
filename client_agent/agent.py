import asyncio
import websockets
import json
import random

SERVER_WS = "ws://127.0.0.1:8000/ws/agent"

async def send_intrusion_data():

    async with websockets.connect(SERVER_WS) as ws:

        while True:

            # dummy intrusion simulation
            packet_rate = random.randint(1, 20)
            failed_logins = random.randint(0, 5)

            data = {
                "packet_rate": packet_rate,
                "failed_logins": failed_logins,
                "client_id": 1
            }

            await ws.send(json.dumps(data))
            print("Sent:", data)

            await asyncio.sleep(5)

asyncio.run(send_intrusion_data())
