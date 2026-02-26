#!/usr/bin/env python3
"""
Data Viewer for KrishiShakti
Shows all stored sensor data in a readable format
"""

import json
import os
from datetime import datetime

def view_data():
    """Display stored sensor data"""
    
    print("╔════════════════════════════════════════════════════════╗")
    print("║  KrishiShakti Data Viewer                             ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # Check if data file exists
    data_file = 'data/history.json'
    
    if not os.path.exists(data_file):
        print("❌ No data found!")
        print(f"   File not found: {data_file}")
        print("\n💡 Make sure:")
        print("   1. Flask server is running: python app.py")
        print("   2. Simulator is running: python simulator.py")
        print("   3. Data has been generated\n")
        return
    
    # Load data
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading data: {str(e)}\n")
        return
    
    if not data or len(data) == 0:
        print("📭 No data stored yet!")
        print("\n💡 Start the simulator to generate data:")
        print("   python simulator.py\n")
        return
    
    # Display summary
    print(f"📊 Total Records: {len(data)}")
    print(f"📅 First Record: {data[0].get('timestamp', 'Unknown')}")
    print(f"📅 Last Record: {data[-1].get('timestamp', 'Unknown')}")
    print("\n" + "="*80 + "\n")
    
    # Display latest 10 records
    print("📋 LATEST 10 RECORDS:\n")
    
    latest = data[-10:] if len(data) > 10 else data
    latest.reverse()  # Show newest first
    
    for i, record in enumerate(latest, 1):
        # Parse timestamp
        timestamp = record.get('timestamp', 'Unknown')
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            time_str = timestamp
        
        # Extract values
        mq135 = record.get('mq135', {}).get('value', 0)
        temp = record.get('dht22', {}).get('temperature', 0)
        humidity = record.get('dht22', {}).get('humidity', 0)
        pm25 = record.get('pms5003', {}).get('pm25', 0)
        pm10 = record.get('pms5003', {}).get('pm10', 0)
        fc28 = record.get('fc28', {}).get('value', 0)
        tds = record.get('tds', {}).get('value', 0)
        
        # Location
        location = record.get('location', {})
        if location:
            city = location.get('city', 'Unknown')
            country = location.get('country', 'Unknown')
            loc_str = f"{city}, {country}"
        else:
            loc_str = "Unknown"
        
        # Display record
        print(f"┌─ Record #{len(data) - i + 1} ─────────────────────────────────────────────┐")
        print(f"│ 🕐 Time: {time_str}")
        print(f"│ 📍 Location: {loc_str}")
        print(f"│")
        print(f"│ 🌡️  Temperature:    {temp:.1f}°C")
        print(f"│ 💧 Humidity:       {humidity:.1f}%")
        print(f"│ 🌿 Air Quality:    {mq135:.1f} ppm")
        print(f"│ 💨 PM2.5:          {pm25:.1f} µg/m³")
        print(f"│ 💨 PM10:           {pm10:.1f} µg/m³")
        print(f"│ 💦 Soil Moisture:  {fc28:.1f}%")
        print(f"│ 🚰 Water Quality:  {tds:.0f} ppm")
        print(f"└────────────────────────────────────────────────────────────┘\n")
    
    # Display statistics
    print("="*80)
    print("\n📈 STATISTICS:\n")
    
    # Calculate averages
    temps = [r.get('dht22', {}).get('temperature', 0) for r in data]
    humidities = [r.get('dht22', {}).get('humidity', 0) for r in data]
    air_qualities = [r.get('mq135', {}).get('value', 0) for r in data]
    moistures = [r.get('fc28', {}).get('value', 0) for r in data]
    
    avg_temp = sum(temps) / len(temps) if temps else 0
    avg_humidity = sum(humidities) / len(humidities) if humidities else 0
    avg_air = sum(air_qualities) / len(air_qualities) if air_qualities else 0
    avg_moisture = sum(moistures) / len(moistures) if moistures else 0
    
    min_temp = min(temps) if temps else 0
    max_temp = max(temps) if temps else 0
    min_moisture = min(moistures) if moistures else 0
    max_moisture = max(moistures) if moistures else 0
    
    print(f"🌡️  Temperature:")
    print(f"   Average: {avg_temp:.1f}°C")
    print(f"   Range: {min_temp:.1f}°C - {max_temp:.1f}°C")
    print()
    
    print(f"💧 Humidity:")
    print(f"   Average: {avg_humidity:.1f}%")
    print()
    
    print(f"🌿 Air Quality:")
    print(f"   Average: {avg_air:.1f} ppm")
    print()
    
    print(f"💦 Soil Moisture:")
    print(f"   Average: {avg_moisture:.1f}%")
    print(f"   Range: {min_moisture:.1f}% - {max_moisture:.1f}%")
    print()
    
    # Status
    if avg_moisture < 30:
        print("⚠️  WARNING: Low soil moisture - watering needed!")
    if avg_temp > 30:
        print("⚠️  WARNING: High temperature detected!")
    if avg_air > 150:
        print("⚠️  WARNING: Poor air quality detected!")
    
    print("\n" + "="*80)
    print(f"\n💾 Data file location: {os.path.abspath(data_file)}")
    print(f"📊 Total size: {os.path.getsize(data_file) / 1024:.1f} KB")
    print()


def export_to_csv():
    """Export data to CSV file"""
    
    data_file = 'data/history.json'
    
    if not os.path.exists(data_file):
        print("❌ No data found to export!\n")
        return
    
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading data: {str(e)}\n")
        return
    
    if not data:
        print("📭 No data to export!\n")
        return
    
    # Create CSV
    csv_file = 'data/sensor_data_export.csv'
    
    with open(csv_file, 'w') as f:
        # Write header
        f.write("Timestamp,Date,Time,Air Quality (ppm),Temperature (°C),Humidity (%),")
        f.write("PM2.5 (µg/m³),PM10 (µg/m³),Soil Moisture (%),Water Quality (ppm),")
        f.write("City,Country,Latitude,Longitude\n")
        
        # Write data
        for record in data:
            timestamp = record.get('timestamp', '')
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                date_str = dt.strftime('%Y-%m-%d')
                time_str = dt.strftime('%H:%M:%S')
            except:
                date_str = ''
                time_str = ''
            
            mq135 = record.get('mq135', {}).get('value', 0)
            temp = record.get('dht22', {}).get('temperature', 0)
            humidity = record.get('dht22', {}).get('humidity', 0)
            pm25 = record.get('pms5003', {}).get('pm25', 0)
            pm10 = record.get('pms5003', {}).get('pm10', 0)
            fc28 = record.get('fc28', {}).get('value', 0)
            tds = record.get('tds', {}).get('value', 0)
            
            location = record.get('location', {})
            city = location.get('city', '') if location else ''
            country = location.get('country', '') if location else ''
            lat = location.get('latitude', '') if location else ''
            lon = location.get('longitude', '') if location else ''
            
            f.write(f"{timestamp},{date_str},{time_str},{mq135:.2f},{temp:.2f},{humidity:.2f},")
            f.write(f"{pm25:.2f},{pm10:.2f},{fc28:.2f},{tds:.0f},")
            f.write(f"{city},{country},{lat},{lon}\n")
    
    print(f"✅ Data exported to: {os.path.abspath(csv_file)}")
    print(f"📊 Total records: {len(data)}")
    print(f"💾 File size: {os.path.getsize(csv_file) / 1024:.1f} KB")
    print("\n💡 You can open this file in Excel or Google Sheets!\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'export':
        export_to_csv()
    else:
        view_data()
        
        print("\n💡 Commands:")
        print("   python view_data.py          - View data")
        print("   python view_data.py export   - Export to CSV")
        print()
