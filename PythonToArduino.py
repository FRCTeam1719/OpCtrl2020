import serial
import serial.tools.list_ports
import serial.serialutil
from networktables import NetworkTables
import time
import sys

class ArduinoInterface:
    def __init__(self):
        print("Waiting for Arduino...")
        while 1:
            arduino_ports = []
            for p in serial.tools.list_ports.comports():
                if 'Arduino' in p.description:
                    arduino_ports.append(p.device) # "COM3"

            if len(arduino_ports) != 0:
                break

        if len(arduino_ports) > 1:
            print("More than one Arduino found, using the first one.")

        arduino_port = arduino_ports[0]

        print("Arduino on port: " + arduino_port)

        self.connection = serial.Serial(arduino_port, 9600)
        if not self.connection.isOpen():
            self.connection.open()

        print("Arduino Interface is now open...")

        self.connection.write(0x00.to_bytes(1, "little"))
        self.connection.write(0x00.to_bytes(1, "little"))

        self.led_count = int.from_bytes(self.connection.read(), "little")

        print("Number of LEDs: " + str(self.led_count))  

    def control(self, id_, val):
        id_ = (id_).to_bytes(1, "little")
        val = (val).to_bytes(1, "little")

        self.connection.write(id_) # id
        self.connection.write(val) # value

    def cleanup(self):
        self.connection.close()

a = ArduinoInterface()

NetworkTables.initialize(server='10.17.19.2')
nt = NetworkTables.getTable('SmartDashboard')

time.sleep(2)

if not NetworkTables.isConnected():
    print("Couldn't connect to NetworkTables, quitting...")
    sys.exit(0)

print("Connected to NetworkTables.")

# generate led controls
num_of_leds = a.led_count
for i in range(num_of_leds):
    nt.putNumber("LED" + str(i+1), 255)

def valueChanged(table, key, value, isNew):
    if not key.startswith("LED"):
        return

    id_ = int(key[3:])
    print("LED ID " + str(id_))

    print(int(value))
    a.control(id_, int(value))

nt.addEntryListener(valueChanged)

while True:
    time.sleep(1)

a.cleanup()