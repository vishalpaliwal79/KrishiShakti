import requests

# Blynk Sync Configuration
BLYNK_TOKEN = "OaGNlIyoI2FG6xTgLeUY1Flz-7fadvjO"
BLYNK_UPDATE_URL = f"https://blynk.cloud/external/api/update?token={BLYNK_TOKEN}"

def hardware_control(device: str, on: bool):
    """
    Physical hardware control interface.
    Replace these print statements with real GPIO, Serial, or Blynk API calls.
    """
    action = "ON" if on else "OFF"
    
    # Blynk API Routing
    pin_map = {
        'pump': 'V20',
        'fan': 'V21'
    }
    
    if device in pin_map:
        pin = pin_map[device]
        val = 1 if on else 0
        try:
            requests.get(f"{BLYNK_UPDATE_URL}&{pin}={val}", timeout=2)
            print(f'[HARDWARE] Sync to Blynk: {device} ({pin}) -> {action}')
        except Exception as e:
            print(f'[HARDWARE] Blynk sync failed: {e}')

    if device == 'pump':
        print(f'[HARDWARE] 💧 Water Pump -> {action}')
    elif device == 'fan':
        print(f'[HARDWARE] 🌬️ Cooling Fan -> {action}')
    elif device == 'peltier':
        print(f'[HARDWARE] ❄️ Peltier Module -> {action}')
    elif device == 'heater':
        print(f'[HARDWARE] 🔥 Heater (Not Installed) -> {action}')
    else:
        print(f'[HARDWARE] Unknown device: {device}')

def get_sensor_reading(sensor_id: str):
    """
    Abstraction for reading actual hardware sensors.
    In production, this would call I2C/Analog/Digital pins.
    """
    # This is a placeholder for actual raw sensor reading logic
    # Real data currently comes in via /api/sensors POST from external source (NodeMCU/Arduino)
    pass
