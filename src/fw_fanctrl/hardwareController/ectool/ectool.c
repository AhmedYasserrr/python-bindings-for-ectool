#include <stdio.h>
#include <stdbool.h>

#define MAX_SENSORS 10

// Simulated sensor temperatures
float sensor_temperatures[MAX_SENSORS] = {45.5, 50.2, 47.8, 55.1, 42.0, 60.3, 51.7, 53.6, 49.4, 46.8};

// List of non-battery sensor IDs
int non_battery_sensors[] = {1, 2, 4};
const int num_non_battery_sensors = sizeof(non_battery_sensors) / sizeof(non_battery_sensors[0]);

// Simulated fan speed percentage (0-100)
int fan_speed = 0;

// Returns space-separated non-battery sensor IDs
const char* get_non_battery_sensors() {
    return "1 2 4";  
}

// Get temperature of a specific sensor
float get_sensor_temperature(int sensor_id) {
    if (sensor_id < 0 || sensor_id >= MAX_SENSORS) {
        fprintf(stderr, "Error: Invalid sensor ID %d\n", sensor_id);
        return -1.0f;  // Return -1.0f as an error indicator since it gets filtered
    }
    return sensor_temperatures[sensor_id];
}

// Get the maximum temperature from all sensors
float get_max_temperature() {
    float max_temp = -1.0f;
    for (int i = 0; i < MAX_SENSORS; i++) {
        if (sensor_temperatures[i] > max_temp) {
            max_temp = sensor_temperatures[i];
        }
    }
    return max_temp;
}

// Get the maximum temperature among non-battery sensors
float get_max_non_battery_temperature() {
    float max_temp = -1.0f;  
    for (int i = 0; i < num_non_battery_sensors; i++) {
        float temp = get_sensor_temperature(non_battery_sensors[i]);
        if (temp > max_temp) {
            max_temp = temp;
        }
    }
    return max_temp;
}

// Set fan speed (0-100%)
void set_fan_speed(int speed) {
    if (speed < 0 || speed > 100) {
        fprintf(stderr, "Error: Fan speed must be between 0 and 100.\n");
        return;
    }
    fan_speed = speed;
}

// Simulated AC status
bool is_on_ac() {
    return true;  
}

void pause_fan_control() {
    // Implementation of enabling automatic fan control
}