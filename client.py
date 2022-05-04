import asyncio
import sys
# sys.path.insert(0, "..")
import logging
import threading
from asyncua import Client, Node, ua
from time import sleep
import keyboard

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

uri = "my_uri"
# url = 'opc.tcp://74.210.169.94:4840'  # Adresse Thomas.
url = 'opc.tcp://localhost:4840/opcua'  # Adresse en localhost.


async def main():
    global uri
    global url
    nb_patates = 0

    async with Client(url=url) as client:
        idx = await client.get_namespace_index(uri)

        activable_node = await client.nodes.root.get_child(["0:Objects", f"{idx}:PLC", f"{idx}:Activable"])
        machine_on_node = await client.nodes.root.get_child(["0:Objects", f"{idx}:PLC", f"{idx}:MachineOn"])
        print("===")
        print(machine_on_node)

        while True:
            machine_on_value = await machine_on_node.read_value()
            activable_value = await activable_node.read_value()

            if keyboard.is_pressed("Alt") and activable_value == 1 and machine_on_value == 0:
                await machine_on_node.write_value(1)

            if machine_on_value == 1:
                sleep(0.2)
                nb_patates += 1
                print(f"J'ai fais {str(nb_patates)} patate(s).")
                if keyboard.is_pressed("Alt"):
                    print("Machine allready running.")
                if keyboard.is_pressed("Ctrl"):
                    print("Machine turned off.")
                    print("======================================================")
                    print("==== VOUS DEVEZ ENTRER UNE RAISON SUR THINGSBOARD ====")
                    print("======================================================")
                    await activable_node.write_value(0)
                    await machine_on_node.write_value(0)

            if activable_value == 0 and machine_on_value == 0:
                activable_value = await activable_node.read_value()


if __name__ == '__main__':
    asyncio.run(main())