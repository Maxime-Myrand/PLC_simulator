import logging
import asyncio
import sys
import random
from time import sleep
sys.path.insert(0, "..")

from asyncua import ua, Server
from asyncua.common.methods import uamethod

nb_reason = 0

async def main():
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840')
    server.set_security_IDs(["Anonymous"])
    server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

    # setup our own namespace, not really necessary but should as spec
    uri = 'my_uri'
    idx = await server.register_namespace(uri)

    # Mes objets
    my_PLC = await server.nodes.objects.add_object(idx, 'PLC')


    # Gestion des variables des objets
    activable = await my_PLC.add_variable(idx, 'Activable', 1)
    patate = await my_PLC.add_variable(idx, 'Patate', 0)
    last_reason = await my_PLC.add_variable(idx, 'LastReason', "Première activation.")
    machine_on = await my_PLC.add_variable(idx, 'MachineOn', 0)

    await my_PLC.add_variable(idx, 'Name', 'Mon Automate')
    await activable.set_writable()
    await last_reason.set_writable()
    await machine_on.set_writable()

    @uamethod
    async def sendReason(parent, reason):
        global nb_reason
        if reason == "" or await activable.read_value() == 1:
            return False

        nb_reason += 1
        await last_reason.write_value(str(nb_reason) + ". " + reason)
        await activable.write_value(1)
        return True

    @uamethod
    async def toggleActivable(parent, arg):
        if arg == False:
            await activable.write_value(0)
            await  machine_on.write_value(0)
        else:
            await activable.write_value(1)
            await  machine_on.write_value(1)

    await my_PLC.add_method(idx, "ToggleActivable", toggleActivable, [], [ua.VariantType.Int32])
    await my_PLC.add_method(idx, "SendReason", sendReason, [ua.VariantType.String], [ua.VariantType.Boolean])

    async with server:
        print("SERVER ON . . . ")

        while True:
            reason = ""
            await asyncio.sleep(3)
            #await server.export_xml([server.nodes.objects], "here.xml")

            activable_state = await activable.read_value()
            if(activable_state == 1):
                nb_patate = await patate.read_value()
                nb_patate += random.randint(0, 10)
                await patate.write_value(nb_patate)
                print(nb_patate)
            else:
                nb_patate = await patate.read_value()
                await patate.write_value(nb_patate)
                print(nb_patate)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)

