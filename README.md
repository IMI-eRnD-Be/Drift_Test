# Drift Test for TA-Slider 

This repository contains a Python-based control and measurement system for actuator characterization.
The script allows precise control of a power supply in the range of 1.5V to 8.5V in order to modify the actuator reference. It simultaneously measures the actuator position using a Mitutoyo digital micrometer (Digimatic interface).
The project includes:

Communication and control of the power supply
Acquisition of position data from the Mitutoyo device via serial interface
Support for Mitutoyo DMX drivers (included in the repository, compatible up to Windows 10)

Additionally, the system enables:

Long-cycle drift testing
Detection and analysis of position drift over time

This tool is intended for automated testing, validation, and long-term stability analysis of electromechanical actuators.

Files:

- [serial_port_client.py](serial_port_client.py): Simple client with a `SerialClient` class and CLI.
- [requirements.txt](requirements.txt): Python package requirements.

Quick start

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # macOS / Linux
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Send a command:

```bash
python serial_port_client.py --port COM3 --baud 9600 --send "*IDN?"
```

Adjust `--port` and `--baud` to your device.

## PowerSupply Loop

`PowerSupply_72_2540_loop.py` sends commands to a power supply in a continuous loop with the ability to read from a second serial port.

### Command sequence:
1. Read from secondary port (client2) with command '1'
2. Send cmd1 to primary port
3. Read from secondary port again with command '1'
4. Send cmd2 to primary port
5. Wait for interval and repeat

### Usage:

```bash
python PowerSupply_72_2540_loop.py --port COM16 --port2 COM3 --interval 60
```

### Options:
- `--port` (required): Primary serial port (e.g., COM16)
- `--port2`: Secondary serial port for additional readings (e.g., COM3)
- `--cmd1`: First command for primary port (default: VSET1:8.50)
- `--cmd2`: Second command for primary port (default: VSET1:1.50)
- `--cmd3`: Command for secondary port (default: 1)
- `--interval`: Loop interval in seconds (default: 60)
- `--baud`: Baud rate (default: 9600)
- `--timeout`: Read timeout in seconds (default: 1.0)
- `--output-file`: Output file for secondary port readings (default: COM3_readings.txt)

The readings from the secondary port are logged with timestamps to the output file.
