import asyncio
import json
import websockets
import random
import time


def get_temperature():
    # returns the current temperature
    return random.randint(30, 45)


def get_door():
    # returns false if door is closed
    return random.choice([True, False])


def get_vent():
    # return false if vent is off
    return random.choice([True, False])


def get_lum():
    # return the current brightness
    return random.randint(0, 100)


async def send_info(websocket, path):
    # Envoyer des informations en WebSocket lorsque la connexion est établie
    while True:

        info = {
            "temperature": get_temperature(), "porte ouverte": get_door(), "ventilateur allume": get_vent(), "luminosite": get_lum()
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
