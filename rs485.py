import time
import serial.tools.list_ports

def get_port():
    ports = serial.tools.list_ports.comports()
    comm_port = "None"
    for port in ports:
        if "USB" in str(port):
            comm_port = str(port).split(" ")[0]
    return comm_port

port_name = get_port()
print(f"Detected port: {port_name}")

try:
    ser = serial.Serial(port=port_name, baudrate=9600)
    print("Port opened successfully")
except Exception as e:
    ser = None
    print(f"Cannot open the port: {e}")

def serial_read_data(ser):
    if ser is not None:
        bytes_to_read = ser.inWaiting()
        if bytes_to_read > 0:
            out = ser.read(bytes_to_read)
            data_array = [b for b in out]
            print(f"Received data: {data_array}")
            if len(data_array) >= 7:
                value = data_array[-4] * 256 + data_array[-3]
                return value
    return 0

relay1_ON  = [2, 6, 0, 0, 0, 255, 200, 91]
relay1_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

def set_device1(state):
    if state:
        ser.write(relay1_ON)
    else:
        ser.write(relay1_OFF)
    time.sleep(1)
    print(f"Read data: {serial_read_data(ser)}")

