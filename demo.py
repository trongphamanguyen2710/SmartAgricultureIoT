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

    def activate_relay(self, relay_id):
        print(f"Relay {relay_id} activated.")
        self.start_time = time.time()

    def deactivate_relay(self, relay_id):
        print(f"Relay {relay_id} deactivated.")

    def send_notification(self, message):
        print(f"Notification: {message}")

    def check_flow_sensor(self, required_flow):
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

# Create an instance of the irrigation system
irrigation_system = IrrigationSystem()

# Simulate the irrigation process
irrigation_system.irrigation_process()
