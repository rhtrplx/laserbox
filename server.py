import asyncio
import json
import websockets
import random
import time
import time
import board
import busio
import adafruit_si7021
import RPi.GPIO as GPIO


class laserbox:

    DOOR_PIN = 18
    FAN_PIN = 23
    LIGHT_PIN = 24

    def read_temperature():
        # returns the current temperature
        i2c = busio.I2C(board.SCL, board.SDA)
        temperature = False
        while temperature == False:
            try:
                sensor = adafruit_si7021.SI7021(i2c)
                temperature = sensor.temperature
            except:
                pass
        # print(sensor.relative_humidity)
        return round(temperature)

    def read_door():
        # returns 1 if door is close
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(laserbox.DOOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        val = GPIO.input(laserbox.DOOR_PIN)
        if val == 0:
            return True
        else:
            return False

    def control_fan(state):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(laserbox.FAN_PIN, GPIO.OUT)
        if state is not True:
            GPIO.output(laserbox.FAN_PIN, GPIO.LOW)
        else:
            GPIO.output(laserbox.FAN_PIN, GPIO.HIGH)
        return state

    def update_light(door_state):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(laserbox.LIGHT_PIN, GPIO.OUT)
        if door_state is not True:
            GPIO.output(laserbox.LIGHT_PIN, GPIO.LOW)
        else:
            GPIO.output(laserbox.LIGHT_PIN, GPIO.HIGH)

    def read_vent():
        # return false if vent is off
        return random.choice([True, False])

    def read_lum():
        # return the current brightness
        return random.randint(0, 100)


async def send_info(websocket, path):
    # Envoyer des informations en WebSocket lorsque la connexion est établie
    while True:

        info = {
            "temperature": laserbox.read_temperature(), "porte ouverte": laserbox.read_door(), "ventilateur allume": laserbox.read_vent(), "luminosite": laserbox.read_lum()
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
