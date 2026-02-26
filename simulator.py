#!/usr/bin/env python3
"""
Sensor Data Simulator for KrishiShakti
Generates random sensor data and sends to Flask server
"""

import requests
import random
import time
import json
from datetime import datetime

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
            print(f'✓ Location detected: {cached_location["city"]}, {cached_location["country"]}\n')
            return cached_location
    except Exception as e:
        print(f'⚠ Could not detect location: {str(e)}')
    
    return None

def generate_sensor_data():
    """Generate realistic random sensor values within specified ranges"""
    data = {
        'mq135': round(18 + random.random() * 2, 2),             # 18-20 ppm (Air Quality)
        'temperature': round(28 + random.random() * 2, 2),       # 28-30°C (DHT22)
        'humidity': round(40 + random.random() * 40, 2),         # 40-80% (DHT22)
        'pm25': round(10 + random.random() * 2, 2),              # 10-12 µg/m³ (PMS5003)
        'pm10': round(10 + random.random() * 2, 2),              # 10-12 µg/m³ (PMS5003)
        'fc28': round(10 + random.random() * 2, 2),              # 10-12% (Water Tank Level)
        'tds': round(100 + random.random() * 50, 0)              # 100-150 ppm (TDS Sensor)
    }
    
    # Add location if available
    location = get_location()
    if location:
        data['location'] = location
    
    return data

def send_data():
    """Send sensor data to Flask server"""
    try:
        data = generate_sensor_data()
        print(f'Sending simulated data: {json.dumps(data, indent=2)}')
        
        response = requests.post(API_URL, json=data, timeout=5)
        
        if response.status_code == 200:
            print('✓ Data sent successfully\n')
        else:
            print(f'✗ Error: {response.status_code}\n')
    except requests.exceptions.ConnectionError:
        print('✗ Error: Cannot connect to server. Is Flask running?\n')
    except Exception as error:
        print(f'✗ Error: {str(error)}\n')

def main():
    print('╔════════════════════════════════════════════════════════╗')
    print('║  Air Purification + Water Generation System           ║')
    print('║  Sensor Data Simulator (Python)                       ║')
    print('╚════════════════════════════════════════════════════════╝\n')
    print('📊 Generating sensor data with specified ranges...')
    print('☁️  Data will be sent to Flask server')
    print('🔄 Sending data every 7-8 seconds\n')
    print('📋 Sensor Ranges:')
    print('   • MQ-135 (Air Quality): 18-20 ppm')
    print('   • PMS5003 (PM2.5/PM10): 10-12 µg/m³')
    print('   • DHT22 (Temperature): 28-30°C')
    print('   • FC-28 (Water Level): 10-12%')
    print('   • TDS (Water Quality): 100-150 ppm')
    print('\nPress Ctrl+C to stop\n')
    
    # Send initial data immediately
    send_data()
    
    # Send data every 7-8 seconds (random interval)
    try:
        while True:
            # Random delay between 7 and 8 seconds
            delay = 7 + random.random()
            time.sleep(delay)
            send_data()
    except KeyboardInterrupt:
        print('\n\n👋 Simulator stopped')

if __name__ == '__main__':
    main()
