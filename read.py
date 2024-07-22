import serial
import time

# Replace 'COM3' with the correct COM port your scale is connected to
ser = serial.Serial(
    port='COM3',         # Change this to your COM port
    baudrate=9600,       # Change this to your scale's baud rate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1            # Timeout for read operations in seconds
)

def read_scale():
    try:
        if ser.is_open:
            print("Serial port is open. Reading data...")
            while True:
                data = ser.readline().decode('utf-8').strip()
                if data:
                    print(f"Weight: {data}")
                time.sleep(1)
        else:
            print("Serial port is not open.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    read_scale()
