import logging
import asyncio
import sys
import keyboard
from time import sleep
sys.path.insert(0, "..")

from asyncua import ua, Server
from asyncua.common.methods import uamethod

@uamethod
def multiply(parent, x, y):
    print("multiply method call with parameters: ", x, y)
    return x * y

@uamethod
def func(parent, value):
    print("Hello world")
    return value * 2

async def main():
    _logger = logging.getLogger('asyncua')
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840/opcua')

    # setup our own namespace, not really necessary but should as spec
    uri = 'my_uri'
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, 'PLC')
    ativable = await myobj.add_variable(idx, 'Activable', 1)
    patates = await myobj.add_variable(idx, "Patates", 0)
    print("=========================")
    print(patates)
    # Set MyVariable to be writable by clients
    await ativable.set_writable()
    await patates.set_writable()
    await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), func, [ua.VariantType.Int64], [ua.VariantType.Int64])
    _logger.info('Starting server!')
    async with server:
        print("SERVER ON . . . ")
        reason = ""
        while True:
            await asyncio.sleep(1)
            await ativable.write_value(0)
            
            if keyboard.is_pressed("Ctrl"):
                reason = input("Donnez une raison expliquant l'arrêt de la machine: ")
            if len(reason) >= 5:
                print("Enter a été pressé (une raison de l'arrêt a été donnée).")
                new_val = 1

                _logger.info(f'Set value of "Activable" to {int(new_val)}')
                await ativable.write_value(new_val)

            nb_patate = await patates.get_value()
            print(nb_patate)


async def change_activable(value):
    if value == 0:
        new_val = 1
    elif value == 1:
        new_val = 0
    return new_val


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)