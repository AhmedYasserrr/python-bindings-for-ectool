# Python Bindings for `ectool`

## Overview

This repo is the first step toward exposing `ectool` (used to control the Framework laptop's Embedded Controller) as a shared library with Python bindings. This avoids the inefficiency of spawning a new CLI process every second, as currently done in  [`fw-fanctrl`](https://github.com/TamtamHero/fw-fanctrl/).

## What's Implemented

- A dummy C library (`ectool.c`) exposing basic functions like:
  - `get_max_temperature()`
  - `get_max_non_battery_temperature()`
  - `get_non_battery_sensor_ids()`
- Python bindings via `ctypes` in `EctoolHardwareController.py`
- Integration with `fw-fanctrl`, replacing CLI calls with function calls
- All C functions return constant values for now (placeholder)

## Changes Made
### 1. C Shared Library and build script 
- Implemented in `hardwareController/ectool/ectool.c`
- `build_libectool.sh` script compiles `ectool.c` into `libectool.so` and installs it to `/usr/local/lib/`
- Provides functions like:
  - `get_max_temperature()`
  - `get_max_non_battery_temperature()`
  - `get_non_battery_sensor_ids()`
  -  Additional utility functions 

### 2. Python Bindings
- Implemented in `hardwareController/EctoolHardwareController.py`
- Uses `ctypes` to load and call functions from `libectool.so`
- Modified functions:
  - `populate_non_battery_sensors`: Now retrieves a space-separated string of non-battery sensor IDs from the C library, instead of parsing all sensor data in Python. This simplifies the logic and avoids regex filtering. In the future, this function may be removed entirely, since the only purpose of these IDs is to calculate the max non-battery temperature—which the C library can now do directly.

  - `get_temperature`: Updated to call two C functions: get_max_temperature() and get_max_non_battery_temperature(). This avoids sending all sensor data to Python and handling it there, which would be less efficient. Offloading the calculation to C is faster and cleaner.
  - Other functions:
    The remaining bindings were straightforward to implement using ctypes.

## Usage

1. Build and install the shared library:

   ```bash
   sudo ./build_libectool.sh
   ```
2. Then run:
   ```bash
   sudo ./install.sh
   ```

## Next Steps
- Implement actual EC access in C
- Expose more EC functionality
- Clean integration with `fw-fanctrl`
