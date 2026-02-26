#!/usr/bin/env python3
"""
Arduino Bridge for KrishiShakti
Reads sensor data from Arduino via serial and sends to Flask server
"""

import serial
import requests
import json
import time

# Configuration
ARDUINO_PORT = '/dev/cu.usbmodem14201'  # Change this to your Arduino port
BAUD_RATE = 9600
API_URL = 'http://localhost:5001/api/sensors'

# Cache location to avoid repeated API calls
cached_location = None

def get_location():
    """Get current location from IP address"""
    global cached_location
    
    if cached_location:
        return cached_location
    
    try:
        print('🌍 Detecting location...')
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            cached_location = {
                'city': data.get('city', 'Unknown'),
                'country': data.get('country_name', 'Unknown'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude')
            }
            print(f'✓ Location: {cached_location["city"]}, {cached_location["country"]}\n')
            return cached_location
    except Exception as e:
        print(f'⚠ Could not detect location: {str(e)}')
    
    return None

def list_serial_ports():
    """List available serial ports"""
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    print('Available ports:')
    for port in ports:
        print(f'  - {port.device}')

def main():
    print('╔════════════════════════════════════════════════════════╗')
    print('║  Arduino Bridge (Python)                              ║')
    print('╚════════════════════════════════════════════════════════╝\n')
    
    # List available ports
    list_serial_ports()
    print()
    
    # Get location once at startup
    location = get_location()
    
    try:
        # Connect to Arduino
        print(f'Connecting to Arduino on {ARDUINO_PORT}...')
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset
        print('✓ Connected to Arduino\n')
        
        while True:
            try:
                # Read line from Arduino
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    
                    if line:
                        try:
                            # Parse JSON data
                            sensor_data = json.loads(line)
                            
                            # Add location to sensor data
                            if location:
                                sensor_data['location'] = location
                            
                            print(f'Received: {sensor_data}')
                            
                            # Send to Flask server
                            response = requests.post(API_URL, json=sensor_data, timeout=5)
                            
                            if response.status_code == 200:
                                print('✓ Data sent to server successfully\n')
                            else:
                                print(f'✗ Server error: {response.status_code}\n')
                                
                        except json.JSONDecodeError:
                            print(f'Invalid JSON: {line}')
                        except requests.exceptions.RequestException as e:
                            print(f'✗ Network error: {str(e)}\n')
                            
            except KeyboardInterrupt:
                print('\n\n👋 Bridge stopped')
                break
            except Exception as e:
                print(f'Error: {str(e)}')
                time.sleep(1)
                
    except serial.SerialException as e:
        print(f'\n✗ Serial port error: {str(e)}')
        print('\nTroubleshooting:')
        print('1. Check if Arduino is connected')
        print('2. Update ARDUINO_PORT in arduino_bridge.py')
        print('3. Close Arduino IDE Serial Monitor if open')
        print('4. Check port permissions (may need sudo on Linux)')
    except Exception as e:
        print(f'\n✗ Error: {str(e)}')

if __name__ == '__main__':
    main()
