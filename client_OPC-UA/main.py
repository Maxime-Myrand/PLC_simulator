import asyncio
import sys
# sys.path.insert(0, "..")
import logging
import threading 
from asyncua import Client, Node, ua
from time import sleep
import keyboard
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

nb_patates = 0
activable = 1
on_off = 0

global check_button
check_button = False

def make_potato():
    global nb_patates
    global activable
    global on_off
    while True:
        print(activable)
        sleep(0.2)
        nb_patates += 1
        print(f"J'ai fais {str(nb_patates)} patate(s).")
        if GPIO.input(29) == GPIO.HIGH:
            activable = 0
            on_off = 0
            print("Machine turned off.")
            break
        if GPIO.input(31) == GPIO.HIGH:
            print("Machine allready running.")

def check_button_pressed():
    if GPIO.input(31) == GPIO.HIGH:
        print("Please give a reason why the machine was turned off.")
    elif GPIO.input(29) == GPIO.HIGH:
        print("The machine is allready off.")
    

async def main():
    global nb_patates
    activable = 1
    on_off = False
    nb_patates = 0
    uri = "my_uri"
    url = 'opc.tcp://localhost:4840/opcua'
    
    
    # Boucle "virtuelle pour simuler le focntionnement de PLC."
    while True:
        sleep(0.1)
        if GPIO.input(31) == GPIO.HIGH and activable == 0:
            print("Please give a reason why the machine was turned off.")
            activale = 0
        elif GPIO.input(31) == GPIO.HIGH and activable == 1:
            print("The machine as been turned on.")
            make_potato()
            activable = 0
            
        if activable == 0:
            try_connect_to_server = True
            while try_connect_to_server:
                check_button_pressed()
                try:
                    async with Client(url=url) as client:
                        while activable == 0:
                            # if response.status != 200:
                            #     return {"error": f"server returned {response.status}"}
                            _logger.info('Children of root are: %r', await client.nodes.root.get_children())
                            idx = await client.get_namespace_index(uri)
                            received_value = await client.nodes.root.get_child(["0:Objects", f"{idx}:PLC", f"{idx}:Activable"])
                            patate = await client.nodes.root.get_child(["0:Objects", f"{idx}:PLC", f"{idx}:Patates"])
                            await patate.write_value(nb_patates)
                            activable = await received_value.read_value()


                            root = client.get_root_node()
                            obj = root.get_child(["0:Objects", "{}:MyObject".format(idx)])

                            res = obj.call_method("{}:multiply".format(idx), 3, "klk")
                            print("method result is: ", res)
                            
                            if activable == 1:
                                try_connect_to_server = False
                                break
                except asyncio.exceptions.TimeoutError or asyncio.exceptions.CancelledError:
                    print("Try connecting to server.")


if __name__ == '__main__':
    asyncio.run(main())