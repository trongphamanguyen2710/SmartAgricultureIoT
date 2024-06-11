print("Sensors and Actuators")

import time
import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort
    # return "/dev/ttyUSB1"

portName = getPort()
print(portName)

try:
    ser = serial.Serial(port=portName, baudrate=9600)
    print("Open successfully")
except Exception as e:
    ser = None
    print(f"Can not open the port: {e}")

def serial_read_data(ser):
    if ser is not None:
        bytesToRead = ser.inWaiting()
        if bytesToRead > 0:
            out = ser.read(bytesToRead)
            data_array = [b for b in out]
            print(data_array)
            if len(data_array) >= 7:
                array_size = len(data_array)
                value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
                return value
            else:
                return -1
    return 0

relay1_ON  = [0, 6, 0, 0, 0, 255, 200, 91]
relay1_OFF = [0, 6, 0, 0, 0, 0, 136, 27]

def setDevice1(state):
    if ser is not None:
        if state:
            ser.write(relay1_ON)
        else:
            ser.write(relay1_OFF)
        time.sleep(1)
        print(serial_read_data(ser))
    else:
        print("Serial port not available.")

soil_temperature =[1, 3, 0, 6, 0, 1, 100, 11]
def readTemperature():
    if ser is not None:
        serial_read_data(ser)
        ser.write(soil_temperature)
        time.sleep(1)
        return serial_read_data(ser)
    else:
        print("Serial port not available.")
        return None

soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]
def readMoisture():
    if ser is not None:
        serial_read_data(ser)
        ser.write(soil_moisture)
        time.sleep(1)
        return serial_read_data(ser)
    else:
        print("Serial port not available.")
        return None

while True:
    if ser is not None:
        print("TEST SENSOR")
        print(readMoisture())
        time.sleep(1)
        print(readTemperature())
        time.sleep(1)
    else:
        print("Serial port not available. Retrying to open the port...")
        try:
            ser = serial.Serial(port=portName, baudrate=9600)
            print("Open successfully")
        except Exception as e:
            print(f"Can not open the port: {e}")
        time.sleep(5)
