import logging
import asyncio
import sys
import keyboard
from time import sleep
sys.path.insert(0, "..")

from asyncua import ua, Server
from asyncua.common.methods import uamethod

async def main():
    _logger = logging.getLogger('asyncua')
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840/opcua')

    # setup our own namespace, not really necessary but should as spec
    uri = 'my_uri'
    idx = await server.register_namespace(uri)

    # Mes objets
    my_PLC = await server.nodes.objects.add_object(idx, 'PLC')


    # Gestion des variables des objets
    activable = await my_PLC.add_variable(idx, 'Activable', 1)
    await activable.set_writable()

    _logger.info('Starting server!')
    async with server:
        print("SERVER ON . . . ")
        while True:
            reason = ""
            await asyncio.sleep(1)
            await activable.write_value(0)
            #await server.export_xml([server.nodes.objects], "here.xml")

            
            if keyboard.is_pressed("Shift"):
                reason = input("Donnez une raison expliquant l'arrêt de la machine: ")
            if len(reason) >= 5:
                print("Enter a été pressé (une raison de l'arrêt a été donnée).")
                new_val = 1
                _logger.info(f'Set value of "Activable" to {int(new_val)}')
                await activable.write_value(new_val)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)