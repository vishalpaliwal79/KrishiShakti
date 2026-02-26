#!/usr/bin/env python3
"""
Google Sheets Integration for KrishiShakti
Automatically sends sensor data to Google Sheets for storage and visualization
"""

import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime
import os

# Google Sheets Configuration
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

class GoogleSheetsManager:
    def __init__(self, credentials_file='credentials.json', spreadsheet_name='KrishiShakti Sensor Data'):
        """Initialize Google Sheets connection"""
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        
    def connect(self):
        """Connect to Google Sheets"""
        try:
            if not os.path.exists(self.credentials_file):
                print(f"❌ Error: {self.credentials_file} not found!")
                print("\n📋 Setup Instructions:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a new project or select existing")
                print("3. Enable Google Sheets API and Google Drive API")
                print("4. Create Service Account credentials")
                print("5. Download JSON key file as 'credentials.json'")
                print("6. Share your Google Sheet with the service account email")
                return False
            
            # Load credentials
            creds = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=SCOPES
            )
            
            # Connect to Google Sheets
            self.client = gspread.authorize(creds)
            
            # Try to open existing spreadsheet or create new one
            try:
                self.spreadsheet = self.client.open(self.spreadsheet_name)
                print(f"✓ Connected to existing spreadsheet: {self.spreadsheet_name}")
            except gspread.SpreadsheetNotFound:
                self.spreadsheet = self.client.create(self.spreadsheet_name)
                print(f"✓ Created new spreadsheet: {self.spreadsheet_name}")
                print(f"📊 Spreadsheet URL: {self.spreadsheet.url}")
            
            # Get or create worksheet
            try:
                self.worksheet = self.spreadsheet.worksheet("Sensor Data")
            except gspread.WorksheetNotFound:
                self.worksheet = self.spreadsheet.add_worksheet(
                    title="Sensor Data",
                    rows=1000,
                    cols=15
                )
                # Add headers
                headers = [
                    'Timestamp',
                    'Date',
                    'Time',
                    'Air Quality (ppm)',
                    'Temperature (°C)',
                    'Humidity (%)',
                    'PM2.5 (µg/m³)',
                    'PM10 (µg/m³)',
                    'Soil Moisture (%)',
                    'Water Quality (ppm)',
                    'City',
                    'Country',
                    'Latitude',
                    'Longitude',
                    'Status'
                ]
                self.worksheet.append_row(headers)
                
                # Format header row
                self.worksheet.format('A1:O1', {
                    'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.2},
                    'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
                    'horizontalAlignment': 'CENTER'
                })
                
                print("✓ Created 'Sensor Data' worksheet with headers")
            
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to Google Sheets: {str(e)}")
            return False
    
    def add_sensor_data(self, sensor_data):
        """Add sensor data row to Google Sheets"""
        try:
            if not self.worksheet:
                print("❌ Not connected to Google Sheets")
                return False
            
            # Parse timestamp
            timestamp = sensor_data.get('timestamp', datetime.now().isoformat())
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
            # Extract location
            location = sensor_data.get('location', {})
            city = location.get('city', 'Unknown') if location else 'Unknown'
            country = location.get('country', 'Unknown') if location else 'Unknown'
            latitude = location.get('latitude', '') if location else ''
            longitude = location.get('longitude', '') if location else ''
            
            # Extract sensor values
            mq135 = sensor_data.get('mq135', {}).get('value', 0)
            temp = sensor_data.get('dht22', {}).get('temperature', 0)
            humidity = sensor_data.get('dht22', {}).get('humidity', 0)
            pm25 = sensor_data.get('pms5003', {}).get('pm25', 0)
            pm10 = sensor_data.get('pms5003', {}).get('pm10', 0)
            fc28 = sensor_data.get('fc28', {}).get('value', 0)
            tds = sensor_data.get('tds', {}).get('value', 0)
            
            # Determine status
            status = 'Good'
            if fc28 < 30 or temp > 35 or mq135 > 200:
                status = 'Warning'
            if fc28 < 20 or temp > 40 or mq135 > 300:
                status = 'Critical'
            
            # Prepare row data
            row = [
                timestamp,
                dt.strftime('%Y-%m-%d'),
                dt.strftime('%H:%M:%S'),
                round(mq135, 2),
                round(temp, 2),
                round(humidity, 2),
                round(pm25, 2),
                round(pm10, 2),
                round(fc28, 2),
                round(tds, 0),
                city,
                country,
                latitude,
                longitude,
                status
            ]
            
            # Append row
            self.worksheet.append_row(row)
            
            # Color code status
            row_number = len(self.worksheet.get_all_values())
            if status == 'Warning':
                self.worksheet.format(f'O{row_number}', {
                    'backgroundColor': {'red': 1, 'green': 0.8, 'blue': 0.2}
                })
            elif status == 'Critical':
                self.worksheet.format(f'O{row_number}', {
                    'backgroundColor': {'red': 1, 'green': 0.2, 'blue': 0.2},
                    'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
                })
            
            print(f"✓ Added data to Google Sheets (Row {row_number})")
            return True
            
        except Exception as e:
            print(f"❌ Error adding data: {str(e)}")
            return False
    
    def get_recent_data(self, limit=100):
        """Get recent sensor data from Google Sheets"""
        try:
            if not self.worksheet:
                return []
            
            all_data = self.worksheet.get_all_records()
            return all_data[-limit:] if len(all_data) > limit else all_data
            
        except Exception as e:
            print(f"❌ Error getting data: {str(e)}")
            return []
    
    def create_dashboard_sheet(self):
        """Create a dashboard sheet with charts and summaries"""
        try:
            # Check if dashboard exists
            try:
                dashboard = self.spreadsheet.worksheet("Dashboard")
                print("✓ Dashboard sheet already exists")
                return True
            except gspread.WorksheetNotFound:
                dashboard = self.spreadsheet.add_worksheet(
                    title="Dashboard",
                    rows=50,
                    cols=10
                )
                
                # Add dashboard title
                dashboard.update('A1', 'KrishiShakti Sensor Dashboard')
                dashboard.format('A1', {
                    'textFormat': {'bold': True, 'fontSize': 18},
                    'horizontalAlignment': 'CENTER'
                })
                dashboard.merge_cells('A1:J1')
                
                # Add summary section
                dashboard.update('A3', 'Latest Readings')
                dashboard.format('A3', {'textFormat': {'bold': True, 'fontSize': 14}})
                
                # Add formulas for latest values
                formulas = [
                    ['Metric', 'Current Value', 'Status'],
                    ['Temperature', '=\'Sensor Data\'!E2', '=IF(\'Sensor Data\'!E2>30,"High","Normal")'],
                    ['Humidity', '=\'Sensor Data\'!F2', '=IF(\'Sensor Data\'!F2<50,"Low","Normal")'],
                    ['Soil Moisture', '=\'Sensor Data\'!I2', '=IF(\'Sensor Data\'!I2<30,"Low","Normal")'],
                    ['Air Quality', '=\'Sensor Data\'!D2', '=IF(\'Sensor Data\'!D2>150,"Poor","Good")'],
                    ['Water Quality', '=\'Sensor Data\'!J2', '=IF(\'Sensor Data\'!J2>500,"High","Good")'],
                ]
                
                dashboard.update('A4:C9', formulas)
                dashboard.format('A4:C4', {'textFormat': {'bold': True}})
                
                print("✓ Created Dashboard sheet")
                return True
                
        except Exception as e:
            print(f"❌ Error creating dashboard: {str(e)}")
            return False
    
    def get_spreadsheet_url(self):
        """Get the URL of the spreadsheet"""
        if self.spreadsheet:
            return self.spreadsheet.url
        return None


# Test function
def test_connection():
    """Test Google Sheets connection"""
    print("╔════════════════════════════════════════════════════════╗")
    print("║  KrishiShakti Google Sheets Integration Test         ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    manager = GoogleSheetsManager()
    
    if manager.connect():
        print("\n✅ Successfully connected to Google Sheets!")
        print(f"📊 Spreadsheet URL: {manager.get_spreadsheet_url()}")
        
        # Create dashboard
        manager.create_dashboard_sheet()
        
        # Test adding sample data
        sample_data = {
            'timestamp': datetime.now().isoformat(),
            'mq135': {'value': 125.5},
            'dht22': {'temperature': 27.8, 'humidity': 65.2},
            'pms5003': {'pm25': 32.1, 'pm10': 45.6},
            'fc28': {'value': 25.3},
            'tds': {'value': 287},
            'location': {
                'city': 'Mumbai',
                'country': 'India',
                'latitude': 19.0760,
                'longitude': 72.8777
            }
        }
        
        print("\n📝 Adding sample data...")
        if manager.add_sensor_data(sample_data):
            print("✅ Sample data added successfully!")
        
        print("\n" + "="*60)
        print("✅ Setup Complete!")
        print("="*60)
        print(f"\n📊 Open your spreadsheet: {manager.get_spreadsheet_url()}")
        print("\n💡 Next steps:")
        print("1. Open the spreadsheet URL above")
        print("2. Check the 'Sensor Data' sheet for data")
        print("3. Check the 'Dashboard' sheet for summaries")
        print("4. Update app.py to use Google Sheets integration")
        
    else:
        print("\n❌ Failed to connect to Google Sheets")
        print("\n📋 Setup Instructions:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project")
        print("3. Enable Google Sheets API and Google Drive API")
        print("4. Create Service Account credentials")
        print("5. Download JSON key file as 'credentials.json'")
        print("6. Run this script again")


if __name__ == '__main__':
    test_connection()
