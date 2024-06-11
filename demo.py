import RPi.GPIO as GPIO
import time

class IrrigationSystem:
    def __init__(self):
        self.state = "IDLE"
        self.flow_sensor = 0
        self.start_time = 0
        self.cycle_data = [
            {
                "cycle": 5,
                "flow1": 20,
                "flow2": 10,
                "flow3": 20,
                "isActive": True,
                "schedulerName": "LỊCH TƯỚI 1",
                "startTime": "18:30",
                "stopTime": "18:40"
            }
        ]
        self.setup_gpio()

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        self.relay_pins = {
            1: 17,  # Relay 1 connected to GPIO17
            2: 27,  # Relay 2 connected to GPIO27
            3: 22,  # Relay 3 connected to GPIO22
            7: 5,   # Relay 7 connected to GPIO5
            8: 6    # Relay 8 connected to GPIO6
        }
        for pin in self.relay_pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def activate_relay(self, relay_id):
        GPIO.output(self.relay_pins[relay_id], GPIO.HIGH)
        print(f"Relay {relay_id} activated.")
        self.start_time = time.time()

    def deactivate_relay(self, relay_id):
        GPIO.output(self.relay_pins[relay_id], GPIO.LOW)
        print(f"Relay {relay_id} deactivated.")

    def send_notification(self, message):
        print(f"Notification: {message}")

    def check_flow_sensor(self, required_flow):
        # Here you should add actual flow sensor reading code
        if self.flow_sensor >= required_flow:
            return True
        return False

    def irrigation_process(self):
        for cycle in self.cycle_data:
            if cycle["isActive"]:
                print("Starting irrigation cycle.")
                self.state = "MIXER1"
                self.activate_relay(1)
                while self.state == "MIXER1":
                    if self.check_flow_sensor(cycle["flow1"]) or time.time() - self.start_time >= 10:
                        self.deactivate_relay(1)
                        self.send_notification("Check flow sensor for Mixer 1")
                        self.state = "MIXER2"
                        self.activate_relay(2)

                while self.state == "MIXER2":
                    if self.check_flow_sensor(cycle["flow2"]) or time.time() - self.start_time >= 10:
                        self.deactivate_relay(2)
                        self.state = "MIXER3"
                        self.activate_relay(3)

                while self.state == "MIXER3":
                    if self.check_flow_sensor(cycle["flow3"]) or time.time() - self.start_time >= 10:
                        self.deactivate_relay(3)
                        self.state = "PUMPIN"
                        self.activate_relay(7)

                while self.state == "PUMPIN":
                    # Assuming no water situation handled here
                    time.sleep(20)
                    self.deactivate_relay(7)
                    self.state = "PUMPOUT"

                while self.state == "PUMPOUT":
                    # Pump out process
                    self.activate_relay(8)
                    time.sleep(10)
                    self.deactivate_relay(8)
                    self.state = "IDLE"

                print("Irrigation cycle complete.")
                time.sleep(1)  # Waiting until the next cycle

# Tạo một đối tượng của hệ thống tưới tiêu
irrigation_system = IrrigationSystem()

# Bắt đầu quá trình tưới tiêu
irrigation_system.irrigation_process()
