"""
serial_port_client.py

Simple, cross-platform example for opening a serial port and sending commands using pyserial.
"""

import argparse
import time
import serial

class SerialClient:
    def __init__(self, port, baudrate=9600, timeout=1, newline='\n', xonxoff=False, rtscts=False, dsrdtr=False):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.newline = newline.encode()
        self._cfg = dict(baudrate=baudrate, timeout=timeout, xonxoff=xonxoff, rtscts=rtscts, dsrdtr=dsrdtr)
        self.ser = None

    def open(self):
        if self.ser and self.ser.is_open:
            return
        self.ser = serial.Serial(self.port, **self._cfg)

    def close(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
            except Exception:
                pass

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def send_command(self, cmd, read_response=True, delay=0.05):
        if not self.ser or not self.ser.is_open:
            raise RuntimeError('Serial port not open')
        if isinstance(cmd, str):
            data = cmd.encode()
        else:
            data = bytes(cmd)
        self.ser.write(data + self.newline)
        self.ser.flush()
        time.sleep(delay)
        if read_response:
            return self.read_response()
        return None

    def read_response(self):
        if not self.ser or not self.ser.is_open:
            return ''
        # read until newline or timeout
        try:
            raw = self.ser.readline()
            return raw.decode(errors='ignore').strip()
        except Exception:
            return ''


def main():
    parser = argparse.ArgumentParser(description='Send a command over serial and print the response')
    parser.add_argument('--port', '-p', required=True, help='Serial port (e.g. COM3 or /dev/ttyUSB0)')
    parser.add_argument('--baud', '-b', type=int, default=9600, help='Baud rate')
    parser.add_argument('--send', '-s', help='Command string to send')
    parser.add_argument('--timeout', '-t', type=float, default=1.0, help='Read timeout in seconds')
    parser.add_argument('--newline', '-n', default='\\n', help='Terminator appended to command (default: \\n)')
    args = parser.parse_args()

    client = SerialClient(args.port, baudrate=args.baud, timeout=args.timeout, newline=args.newline)
    with client:
        if args.send:
            resp = client.send_command(args.send)
            print(resp)
        else:
            print('Connected to', args.port)


if __name__ == '__main__':
    main()
