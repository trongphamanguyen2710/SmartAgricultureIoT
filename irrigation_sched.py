import json
from datetime import datetime
import time
from rs485 import *

MIXER_1 = 1
MIXER_2 = 2
MIXER_3 = 3
AREA_SELECTOR_1 = 4
AREA_SELECTOR_2 = 5
AREA_SELECTOR_3 = 6
PUMP_IN = 7
PUMP_OUT = 8

# Load the schedule from the JSON file
def load_schedule(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Get the current time
def get_current_time():
    print("Time: ",datetime.now().strftime('%H:%M:%S'))
    return datetime.now().strftime('%H:%M:%S')


# Check if the current time matches any schedule
def check_schedule(schedule):
    current_time = get_current_time()
    for entry in schedule:
        if entry['startTime'] == current_time:
            return entry
    return None


# Execute the irrigation sequence
def execute_irrigation(entry):
    print(f"Executing irrigation for schedule: {entry['schedulerName']}")
    print("Wait until the start of irrigation")
    count = 1
    while entry['cycle'] >= count:
        print("Mixer 1 is started")
        set_device1(True)
        time.sleep(entry['flow1'])
        set_device1(False)

        print("Mixer 2 is started")
        set_device1(True)
        time.sleep(entry['flow2'])
        set_device1(False)
        print("Mixer 3 is started")
        set_device1(True)
        time.sleep(entry['flow3'])
        set_device1(False)
        print("Pump in is started")
        set_device1(True)
        time.sleep(5)
        set_device1(False)
        print("Pump out is started")
        set_device1(True)
        time.sleep(5)
        set_device1(False)
        print("Wait until the next cycle")
        time.sleep(1)
        count = count + 1
    print("Wait until the end of irrigation")


# Main function
def main():
    schedule_file = 'sched.json'  # Path to your JSON file
    schedule = load_schedule(schedule_file)

    while True:
        entry = check_schedule(schedule)
        if entry:
            execute_irrigation(entry)
        time.sleep(1)  # Check every second


if __name__ == "__main__":
    main()
