#!/usr/bin/env python3
"""
Blynk to KrishiShakti Bridge
Fetches real sensor data from Blynk and sends to local dashboard
"""

import requests
import time
import json
from datetime import datetime

# Blynk Configuration
BLYNK_TOKEN = "OaGNlIyoI2FG6xTgLeUY1Flz-7fadvjO"
# getAll endpoint is more efficient (single request)
BLYNK_GET_URL = f"https://blynk.cloud/external/api/getAll?token={BLYNK_TOKEN}"
BLYNK_UPDATE_URL = f"https://blynk.cloud/external/api/update?token={BLYNK_TOKEN}"

# Pins to fetch (V6 Hum added back)
PINS = ["V3", "V4", "V6", "V7", "V8"]

# Local KrishiShakti Server
LOCAL_SERVER = "http://localhost:5000/api/sensors"

# Mapping Blynk pins to sensor data
# Based on Friend's HARDWARE Setup:
# V3  = Soil Moisture (%)
# V4  = Ultrasonic Distance (cm) -> Water Tank Level
# V7  = Temperature (DHT11)
# V8  = Gas Status (Binary 0/1)
# V6  = Humidity (Optional)
#
# Control Pins (KrishiShakti -> Blynk):
# V20 = Automation Irrigation (Pump)
# V21 = Cooling Chamber Motor

def fetch_blynk_data():
    """Fetch all data from Blynk in a single request"""
    try:
        response = requests.get(BLYNK_GET_URL, timeout=10)
        if response.status_code == 200:
            return response.json() # Returns {"v3": val, "v4": val, ...}
        else:
            print(f"❌ Blynk API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error fetching from Blynk: {str(e)}")
        return None

def sync_control_to_blynk():
    """Sync local device states to Blynk cloud"""
    try:
        from device_controller import get_all
        devices = get_all()
        
        # Mapping KrishiShakti devices to Blynk Pins
        mappings = {
            'pump': 'V20',
            'fan': 'V21'
        }
        
        for dev, pin in mappings.items():
            if dev in devices:
                val = 1 if devices[dev].get('on') else 0
                url = f"{BLYNK_UPDATE_URL}{BLYNK_TOKEN}&{pin}={val}"
                requests.get(url, timeout=3)
    except Exception as e:
        print(f"⚠️  Control sync error: {e}")

def convert_to_krishishakti_format(blynk_data):
    """Convert Blynk data to KrishiShakti format (lowercase keys from getAll)"""
    
    # Target structure for app.py /api/sensors
    # getAll returns lowercase 'v3', 'v4', etc.
    soil_percent = blynk_data.get('v3', 0)
    distance     = blynk_data.get('v4', 0)
    temp         = blynk_data.get('v7', 0)
    gas_binary   = blynk_data.get('v8', 0)
    humidity     = blynk_data.get('v6', None)
    
    # Map to KrishiShakti schema
    # mq135 (Gas): v8=1 is Normal (50.0), v8=0 is Leak (500.0)
    return {
        'temperature': float(temp) if temp is not None else None,
        'humidity': float(humidity) if humidity is not None else None,
        'mq135': 50.0 if int(gas_binary or 0) == 1 else 500.0,
        'fc28': float(distance) if distance is not None else 0.0,
        'tds': float(soil_percent) if soil_percent is not None else 0.0,
        'location': {
            'city': 'Landran',
            'country': 'India',
            'latitude': 30.698,
            'longitude': 76.667
        }
    }

def send_to_krishishakti(data):
    """Send data to local KrishiShakti server"""
    try:
        response = requests.post(LOCAL_SERVER, json=data, timeout=5)
        if response.status_code == 200:
            return True
        else:
            print(f"❌ KrishiShakti API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending to KrishiShakti: {str(e)}")
        return False

def main():
    print("╔════════════════════════════════════════════════════════╗")
    print("║  Blynk to KrishiShakti Bridge                         ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("📡 Fetching real sensor data from Blynk...")
    print("🔄 Sending to KrishiShakti dashboard...")
    print("📍 Location: Landran, Punjab, India")
    print("💾 Saving backup to sensor_data.json\n")
    print("Press Ctrl+C to stop\n")
    
    success_count = 0
    error_count = 0
    
    while True:
        try:
            # Fetch from Blynk
            blynk_data = fetch_blynk_data()
            
            if blynk_data:
                # Save raw Blynk data to JSON file (backup)
                try:
                    with open("sensor_data.json", "w") as file:
                        json.dump(blynk_data, file, indent=4)
                except Exception as e:
                    print(f"⚠️  Could not save to JSON: {str(e)}")
                
                # Convert format
                krishishakti_data = convert_to_krishishakti_format(blynk_data)
                
                # Send to local server
                if send_to_krishishakti(krishishakti_data):
                    success_count += 1
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{current_time}] ✓ "
                          f"T: {krishishakti_data['temperature']}°C, "
                          f"H: {krishishakti_data['humidity'] or '--'}%, "
                          f"Gas: {krishishakti_data['mq135']}, "
                          f"Dist: {krishishakti_data['fc28']}cm, "
                          f"Soil: {krishishakti_data['tds']}%")
                
                # Sync controls back to Blynk
                sync_control_to_blynk()
            else:
                error_count += 1
            
            # 5s interval for stability
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n\n👋 Data collection stopped")
            print(f"\n📊 Statistics:")
            print(f"   ✅ Successful updates: {success_count}")
            print(f"   ❌ Failed updates: {error_count}")
            break
        except Exception as e:
            error_count += 1
            print(f"❌ Error: {str(e)}")
            time.sleep(3)

if __name__ == '__main__':
    main()
