import serial.tools.list_ports


def findComPort():
    """
    Find open Com port with description containing "Arduino"
    """
    ports = list(serial.tools.list_ports.comports())
    for p in ports:

        if "Arduino" in p.description:
            return p.device