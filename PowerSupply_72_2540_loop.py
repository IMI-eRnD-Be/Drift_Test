"""
PowerSupply_72_2540_loop.py

Send the command "VSET1:8.50" to a power supply over serial every minute.
This reuses the `SerialClient` in `serial_port_client.py` (same folder).
"""

import time
import argparse
from serial_port_client import SerialClient



def run_loop(port, baud=9600, interval=60.0, newline='\n', timeout=1.0, cmd1='VSET1:8.50', cmd2='VSET1:1.50', port2=None, cmd3='1', output_file='COM3_readings.txt'):
	with SerialClient(port, baudrate=baud, timeout=timeout, newline=newline) as client:
		print(f"Opened {port} @ {baud} baud. Sending {cmd1} and {cmd2} every {interval} seconds each.")
		
		# Open second serial port if provided
		client2 = None
		if port2:
			client2 = SerialClient(port2, baudrate=baud, timeout=timeout, newline='\r\n')
			client2.open()
			print(f"Opened {port2} @ {baud} baud. Sending {cmd3} every {interval} seconds.")
		
		try:
			while True:
				# Send to client2, then cmd1
				if client2:
					resp = client2.send_command(cmd3, read_response=True)
					timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
					print(f"{timestamp} Sent {cmd3} to {port2}, response: {resp}")
					with open(output_file, 'a') as f:
						f.write(f"{timestamp} - Command: {cmd3} - Response: {resp}\n")
				
				resp = client.send_command(cmd1, read_response=True)
				print(time.strftime('%Y-%m-%d %H:%M:%S'), f'Sent {cmd1}, response:', resp)
				
				# Send to client2 again, then cmd2
				if client2:
					resp = client2.send_command(cmd3, read_response=True)
					timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
					print(f"{timestamp} Sent {cmd3} to {port2}, response: {resp}")
					with open(output_file, 'a') as f:
						f.write(f"{timestamp} - Command: {cmd3} - Response: {resp}\n")
				
				resp = client.send_command(cmd2, read_response=True)
				print(time.strftime('%Y-%m-%d %H:%M:%S'), f'Sent {cmd2}, response:', resp)
				
				# Wait for interval
				time.sleep(interval)
		except KeyboardInterrupt:
			print("Interrupted by user, closing serial ports.")
		finally:
			if client2:
				client2.close()


def main():
	parser = argparse.ArgumentParser(description='Loop sender for power supply VSET1 command.')
	parser.add_argument('--port', '-p', required=True, help='Serial port (e.g. COM16 or /dev/ttyUSB0)')
	parser.add_argument('--port2', '-p2', default=None, help='Second serial port (e.g. COM3) for additional readings')
	parser.add_argument('--baud', '-b', type=int, default=9600, help='Baud rate')
	parser.add_argument('--interval', '-i', type=float, default=60.0, help='Loop interval in seconds')
	parser.add_argument('--cmd1', default='VSET1:8.50', help='First command to send')
	parser.add_argument('--cmd2', default='VSET1:1.50', help='Second command to send')
	parser.add_argument('--cmd3', default='1', help='Command to send to second port')
	parser.add_argument('--output-file', '-o', default='COM3_readings.txt', help='Output file for COM3 readings')
	parser.add_argument('--newline', '-n', default='\\n', help='Terminator appended to command')
	parser.add_argument('--timeout', '-t', type=float, default=1.0, help='Read timeout in seconds')
	args = parser.parse_args()

	run_loop(args.port, args.baud, args.interval, args.newline, args.timeout, args.cmd1, args.cmd2, args.port2, args.cmd3, args.output_file)


if __name__ == '__main__':
	main()