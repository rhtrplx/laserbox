import asyncio
import json
import websockets
import random
import time


async def send_info(websocket, path):
    # Envoyer des informations en WebSocket lorsque la connexion est établie
    while True:

        info = {
            "temp": random.randint(20, 45), "gate": random.choice([True, False]), "vent": random.randint(100, 2000)
        }
        info_json = json.dumps(info)
        await websocket.send(info_json)
        print(f"Envoi d'informations en WebSocket : {info_json}")

        time.sleep(1)


async def main():
    # Lancer un serveur WebSocket sur le port 8080
    async with websockets.serve(send_info, "localhost", 8080):
        print("Serveur WebSocket lancé sur ws://localhost:8080")

        # Boucle d'événements asyncio
        await asyncio.Future()

# Exécuter la boucle d'événements asyncio
asyncio.run(main())
