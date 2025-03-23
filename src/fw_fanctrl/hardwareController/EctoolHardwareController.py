from abc import ABC
import ctypes
from fw_fanctrl.hardwareController.HardwareController import HardwareController


class EctoolHardwareController(HardwareController, ABC):
    noBatterySensorMode = False
    nonBatterySensors = None
    ectool = None
    def __init__(
        self, 
        no_battery_sensor_mode=False, 
        ectool_lib_path= "/usr/local/lib/libectool.so"
    ):
        self.ectool = ctypes.CDLL(ectool_lib_path)
        self._initialize_ectool_functions()
        if no_battery_sensor_mode:
            self.noBatterySensorMode = True
            self.populate_non_battery_sensors()

    def _initialize_ectool_functions(self):
        """Define ctypes function signatures for ectool library."""
        self.ectool.get_non_battery_sensors.restype = ctypes.c_char_p

        self.ectool.get_sensor_temperature.argtypes = [ctypes.c_int]
        self.ectool.get_sensor_temperature.restype = ctypes.c_float

        self.ectool.set_fan_speed.argtypes = [ctypes.c_int]
        self.ectool.set_fan_speed.restype = None

        self.ectool.get_max_temperature.restype = ctypes.c_float
        self.ectool.get_max_non_battery_temperature.restype = ctypes.c_float

        self.ectool.is_on_ac.restype = ctypes.c_bool
        self.ectool.pause_fan_control.restype = None

    def populate_non_battery_sensors(self):
        raw_out = self.ectool.get_non_battery_sensors().decode("utf-8")  
        
        # Assuming the C function returns space-separated IDs
        self.nonBatterySensors = list(map(int, raw_out.split())) 

    def get_temperature(self):
        if self.noBatterySensorMode:
            max_temp = self.ectool.get_max_non_battery_temperature()

            # Alternative approach: Manually retrieve and sort non-battery sensor temperatures.
            # Less efficient method than calling get_max_non_battery_temperature().

            # temps = [self.ectool.get_sensor_temperature(sensor) for sensor in self.nonBatterySensors]
            # sorted([temp for temp in temps if temp > 0], reverse=True)
            # max_temp = temps[0] if temps else 50
        else:
            max_temp = self.ectool.get_max_temperature()
 
        # safety fallback to avoid damaging hardware
        if max_temp < 0:
            return 50
        return float(round(max_temp, 2))

    def set_speed(self, speed):
        self.ectool.set_fan_speed(speed)

    def is_on_ac(self):
        return self.ectool.is_on_ac()

    def pause(self):
        self.ectool.pause_fan_control()

    def resume(self):
        # Empty for ectool, as setting an arbitrary speed disables the automatic fan control
        pass


# ====================== MAIN FUNCTION FOR TESTING ======================
def main():
    print("Running actual hardware tests...\n")

    # Initialize the controller with real hardware access
    ectool_path = "./ectool/libectool.so"
    print(f"Using ectool library at: {ectool_path}")
    controller = EctoolHardwareController(ectool_lib_path=ectool_path)

    # Test fetching temperature
    temp = controller.get_temperature()
    print(f"Max temperature: {temp}°C")

    # Test non-battery mode
    controller_no_batt = EctoolHardwareController(no_battery_sensor_mode=True, ectool_lib_path=ectool_path)
    temp_no_batt = controller_no_batt.get_temperature()
    print(f"Max non-battery temperature: {temp_no_batt}°C")

    # Test setting fan speed
    print("Setting fan speed to 50%...")
    controller.set_speed(50)

    # Test AC power status
    ac_status = controller.is_on_ac()
    print(f"Running on AC power: {'Yes' if ac_status else 'No'}")

    # Test pausing fan control
    print("Pausing fan control...")
    controller.pause()

    # Test resuming fan control
    print("Resuming fan control...")
    controller.resume()

    print("\nHardware tests completed.")

if __name__ == "__main__":
    main()  
  
