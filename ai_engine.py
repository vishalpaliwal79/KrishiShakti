"""
KrishiShakti AI Decision Engine
Hardware-aware, sensor-validated, demo-ready
"""
from datetime import datetime
import json, os

# ─── Hardware manifest — set False for devices not physically present ──────────
HARDWARE = {
    'pump':    True,
    'fan':     True,
    'peltier': False,
    'heater':  False,   # NOT installed — AI will never suggest this
}

# ─── Realistic thresholds ─────────────────────────────────────────────────────
T = {
    'moisture_critical': 25,   # irrigate immediately
    'moisture_low':      40,   # irrigate soon
    'moisture_optimal':  60,   # target level
    'moisture_high':     75,   # skip irrigation
    'temp_warm':         28,   # fan low speed
    'temp_hot':          33,   # fan high speed
    'humidity_awg_min':  50,   # minimum humidity to run AWG
    'humidity_fan_skip': 70,   # high humidity — reduce fan use
    'tank_full':         88,   # stop AWG
    'tank_low':          20,   # alert
}

# ─── Sensor validity check ────────────────────────────────────────────────────
def _validate(moisture, temperature, humidity, tank_level):
    """
    Returns (valid: bool, issues: list[str])
    A reading is invalid if it is zero, None, or clearly out of range.
    """
    issues = []
    if not moisture    or moisture    <= 0:  issues.append('Soil moisture sensor not reading')
    if not temperature or temperature <= 0:  issues.append('Temperature sensor not reading')
    if not humidity    or humidity    <= 0:  issues.append('Humidity sensor not reading')
    if moisture    and not (0 < moisture    <= 100): issues.append(f'Moisture out of range ({moisture}%)')
    if temperature and not (0 < temperature <= 60):  issues.append(f'Temperature out of range ({temperature}°C)')
    if humidity    and not (0 < humidity    <= 100): issues.append(f'Humidity out of range ({humidity}%)')
    return len(issues) == 0, issues


# ─── Main AI decision function ────────────────────────────────────────────────
def ai_decision(moisture, temperature, humidity, hour=None, tank_level=0):
    """
    Hardware-aware AI decision engine.
    Returns clean JSON-serialisable dict — never suggests unavailable devices.
    """
    if hour is None:
        hour = datetime.now().hour

    # ── Validate sensors first ────────────────────────────────────────────────
    valid, issues = _validate(moisture, temperature, humidity, tank_level)
    if not valid:
        return {
            'valid':       False,
            'actions':     {},
            'decisions':   {},
            'explanation': [f'⚠️ {i}' for i in issues],
            'env_state':   'Waiting',
            'confidence':  0,
            'timestamp':   datetime.now().isoformat(),
            'inputs':      {'moisture': moisture, 'temperature': temperature,
                            'humidity': humidity, 'tank_level': tank_level},
            'sensor_warning': '⚠️ Waiting for valid sensor data — AI decisions paused'
        }

    actions      = {}
    decisions    = {}   # rich dict for device_controller
    explanations = []
    confidence   = 90

    # ── Pump / Irrigation ─────────────────────────────────────────────────────
    if HARDWARE['pump']:
        if moisture < T['moisture_critical']:
            pump_on  = True
            duration = _calc_duration(moisture, temperature, humidity)
            explanations.append(f'🚨 Soil moisture critically low ({moisture:.0f}%) — irrigation started immediately')
            confidence = min(confidence, 97)
        elif moisture < T['moisture_low']:
            pump_on  = True
            duration = _calc_duration(moisture, temperature, humidity)
            explanations.append(f'💧 Soil moisture low ({moisture:.0f}%) — irrigation needed for {duration} min')
            confidence = min(confidence, 92)
        elif moisture >= T['moisture_high']:
            pump_on  = False
            duration = 0
            explanations.append(f'✅ Soil moisture sufficient ({moisture:.0f}%) — irrigation not needed')
        else:
            pump_on  = False
            duration = 0
            explanations.append(f'✅ Soil moisture optimal ({moisture:.0f}%) — no irrigation required')

        actions['pump']   = 'on' if pump_on else 'off'
        decisions['pump'] = {'on': pump_on, 'duration_min': duration}

    # ── Fan / Cooling ─────────────────────────────────────────────────────────
    if HARDWARE['fan']:
        # Reduce fan use when humidity is already high (prevents over-drying)
        high_humidity = humidity >= T['humidity_fan_skip']

        if temperature >= T['temp_hot'] and not high_humidity:
            fan_on = True
            speed  = 'high'
            explanations.append(f'🌡️ Temperature high ({temperature:.0f}°C) — cooling fan ON at high speed')
        elif temperature >= T['temp_warm'] and not high_humidity:
            fan_on = True
            speed  = 'low'
            explanations.append(f'🌡️ Temperature warm ({temperature:.0f}°C) — cooling fan ON at low speed')
        elif temperature >= T['temp_warm'] and high_humidity:
            fan_on = False
            speed  = 'off'
            explanations.append(f'🌡️ Temperature warm but humidity high ({humidity:.0f}%) — fan kept OFF to retain moisture')
        else:
            fan_on = False
            speed  = 'off'
            explanations.append(f'🌡️ Temperature normal ({temperature:.0f}°C) — fan not needed')

        actions['fan']   = 'on' if fan_on else 'off'
        decisions['fan'] = {'on': fan_on, 'speed': speed}

    # ── Heater — NOT available, never suggest ─────────────────────────────────
    # HARDWARE['heater'] is False — completely skipped

    # ── Peltier / AWG ─────────────────────────────────────────────────────────
    if HARDWARE['peltier']:
        tank_full    = tank_level >= T['tank_full']
        enough_humid = humidity   >= T['humidity_awg_min']

        if tank_full:
            peltier_on = False
            awg_mode   = 'off'
            explanations.append(f'🛑 Water tank full ({tank_level:.0f}%) — AWG stopped automatically')
        elif enough_humid:
            peltier_on = True
            awg_mode   = 'awg'
            explanations.append(f'💧 Humidity good ({humidity:.0f}%) — AWG generating water')
            if tank_level < T['tank_low']:
                explanations.append(f'⚠️ Tank level low ({tank_level:.0f}%) — AWG running at full capacity')
        else:
            peltier_on = False
            awg_mode   = 'off'
            explanations.append(f'🏜️ Humidity too low ({humidity:.0f}%) — AWG paused, not enough moisture in air')
            confidence = min(confidence, 80)

        actions['peltier']   = 'on' if peltier_on else 'off'
        decisions['peltier'] = {'on': peltier_on, 'awg_mode': awg_mode}

    # ── Environment state label ───────────────────────────────────────────────
    if temperature >= T['temp_hot']:
        env_state = 'Cooling'
    elif humidity >= T['humidity_fan_skip']:
        env_state = 'Humid'
    else:
        env_state = 'Normal'

    return {
        'valid':          True,
        'actions':        actions,          # simple on/off per device
        'decisions':      decisions,        # rich dict for device_controller
        'explanation':    explanations,
        'env_state':      env_state,
        'confidence':     confidence,
        'timestamp':      datetime.now().isoformat(),
        'inputs': {
            'moisture':    moisture,
            'temperature': temperature,
            'humidity':    humidity,
            'hour':        hour,
            'tank_level':  tank_level,
        },
        'hardware':       HARDWARE,         # tell frontend which devices exist
    }


def _calc_duration(moisture, temperature, humidity):
    """Irrigation duration in minutes — capped 5–45 min"""
    deficit        = max(0, T['moisture_optimal'] - moisture)
    base           = deficit * 0.35
    temp_factor    = 1 + max(0, temperature - 25) * 0.02
    humidity_factor = max(0.5, 1 - max(0, humidity - 60) * 0.01)
    return round(max(5, min(45, base * temp_factor * humidity_factor)), 1)




# ─── Irrigation log ───────────────────────────────────────────────────────────
from database import insert_irrigation_log, get_irrigation_logs

def log_irrigation(event: dict):
    """Log an irrigation event to SQLite database"""
    insert_irrigation_log(event)

def get_irrigation_history(limit=50):
    """Retrieve irrigation history from SQLite database"""
    return get_irrigation_logs(limit)
