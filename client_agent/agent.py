import asyncio
import websockets
import json
import random

SERVER_WS = "ws://127.0.0.1:8000/ws/agent"

async def send_intrusion_data():

    async with websockets.connect(SERVER_WS) as ws:

        while True:

            # Simulate a continuous Brute Force Attack
            packet_rate = random.randint(30, 60)
            failed_logins = random.randint(8, 15)

            data = {
                "agent_id": 1,
                "ip": "203.0.113.5", # External IP mimicking attacker
                "event": "Brute Force Simulation",
                "action": "Attempt",
                "details": "High volume of failed login attempts",
                "packet_rate": packet_rate,
                "failed_logins": failed_logins
            }

            await ws.send(json.dumps(data))
            print("Sent:", data)

            await asyncio.sleep(5)

asyncio.run(send_intrusion_data())
