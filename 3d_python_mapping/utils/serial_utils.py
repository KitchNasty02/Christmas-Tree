import serial.tools.list_ports
import time



def try_again(seconds):
    for sec in range (seconds, 0, -1):
        if sec > 1:
            print(f"Trying again in {sec}", end='\r')
        else:
            print(f"Trying again in {sec}")

        time.sleep(1)


def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found.")
        return []
    
    print("Available serial ports:")
    for port in ports:
        print(f"  Port: {port.device}")
        print(f"    Description: {port.description}")
        print(f"    Hardware ID: {port.hwid}")
    return ports


def find_arduino_port():
    port_found = False

    while not port_found:
        ports = serial.tools.list_ports.comports()
    
        if not ports:
            print("No serial ports found.")
        else:
            print("Ports Found")
            for port in ports:
                if "CH340" in port.description:
                    print(f"Found Arduino at port: {port.device}")
                    return port.device
                
            print("Arudino port 'CH340' not found")
            list_serial_ports()
        
        try_again(3)








