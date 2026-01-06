import serial
import threading
import queue
import time
import re

# handles all serial events
class SerialManager:
    def __init__(self, baud_rate=9600):
        self.baud_rate = baud_rate
        self.ser = None
        self.queue = queue.Queue()
        self.thread = None
        self.running = False

    # tries to connect to arduino
    def connect(self):
        from utils.serial_utils import find_arduino_port
        port = find_arduino_port()
        
        try:
            self.ser = serial.Serial(port, self.baud_rate, timeout=1)
            # Add a short delay to ensure the Arduino has time to reset
            time.sleep(2)
            print(f"Connected to Arduino on port {port}")
            
            self.running = True
            self.thread = threading.Thread(target=self._read_thread, daemon=True)
            self.thread.start()
            return True
        
        except serial.SerialException as e:
            print(f"Failed to connect to {port}: {e}")
            return False
        

    # worker thread to read serial data
    def _read_thread(self):
        while self.running and self.ser and self.ser.is_open:
            try:
                data = self.ser.readline().decode('utf-8').strip()
                if data and re.match("[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+", data):
                    self.queue.put(data)

            except Exception as e:
                print(f"Serial thread error: {e}")
                self.running = False
                break

            time.sleep(0.01)

    # retrieves an item from queue if avaliable
    def get_data(self):
        if not self.queue.empty():
            return self.queue.get()
        else:
            return None
        
    # close serial connection and stops thread
    def close(self):
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        if self.thread:
            self.thread.join(timeout=1)
        print("Serial mananger shut down")

            
        



