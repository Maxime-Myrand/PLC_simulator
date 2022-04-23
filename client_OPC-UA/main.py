import asyncio
import sys
# sys.path.insert(0, "..")
import logging
from asyncua import Client, Node, ua
from time import sleep
import keyboard

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

async def main():
    uri = "my_uri"
    activable = 1
    on_off = False
    nb_patates = 0
    url = 'opc.tcp://localhost:4840/opcua'

    # Boucle "virtuelle pour simuler le focntionnement de PLC."
    while True:
        if not on_off:
            while True:
                button_pressed = input("Mise en marche? (m): ")
                print(str(activable))
                if activable == 0 and button_pressed == "m":
                    print("Veuillez fournir une raison expliquant l'arrêt de la machine.")
                elif activable == 1 and button_pressed == "m":
                    print("Mise en marche de la machine.")
                    on_off = True
                    break

        while on_off:
            sleep(1)
            nb_patates += 1
            print(f"J'ai fais {str(nb_patates)} patate(s).")
            if keyboard.is_pressed("Alt"):
                activable = 0
                on_off = False

        if activable == 0:
            try_connect_to_server = True
            while try_connect_to_server:
                try:
                    async with Client(url=url) as client:
                        while activable == 0:
                            # if response.status != 200:
                            #     return {"error": f"server returned {response.status}"}
                            _logger.info('Children of root are: %r', await client.nodes.root.get_children())
                            idx = await client.get_namespace_index(uri)
                            received_value = await client.nodes.root.get_child(["0:Objects", f"{idx}:PLC", f"{idx}:Activable"])
                            activable = await received_value.read_value()
                            print("Activable = " + str(activable))
                            if activable == 1:
                                try_connect_to_server = False
                                break
                except asyncio.exceptions.TimeoutError or asyncio.exceptions.CancelledError:
                    print("Try connecting to server.")

        if keyboard.is_pressed('q'):
            exit()


if __name__ == '__main__':
    asyncio.run(main())