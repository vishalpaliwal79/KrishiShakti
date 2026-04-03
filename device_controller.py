"""
KrishiShakti Device Controller
Manages pump, fan, heater, peltier state + manual overrides
"""
import json, os
from datetime import datetime

DEVICES_FILE = os.path.join('data', 'devices.json')

# Default device state — only physically available devices
_default_state = {
    'pump':    {'on': False, 'duration_min': 0, 'last_changed': None},
    'fan':     {'on': False, 'speed': 'off',   'last_changed': None},
}

def _load():
    if os.path.exists(DEVICES_FILE):
        try:
            with open(DEVICES_FILE) as f:
                return json.load(f)
        except:
            pass
    return {k: dict(v) for k, v in _default_state.items()}

def _save(state):
    os.makedirs('data', exist_ok=True)
    with open(DEVICES_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_all():
    return _load()

def set_device(device: str, on: bool, mode: str = 'manual', **kwargs):
    """Set a device on/off — rejects devices not in the hardware manifest"""
    from ai_engine import HARDWARE
    if device not in HARDWARE or not HARDWARE.get(device):
        return {'success': False, 'error': f'Device "{device}" is not available in this hardware setup'}
    state = _load()
    if device not in state:
        return {'success': False, 'error': f'Unknown device: {device}'}
    state[device].update({'on': on, 'last_changed': datetime.now().isoformat()})
    state[device].update(kwargs)
    _save(state)
    
    from database import insert_device_log
    insert_device_log(device, action='turn_on' if on else 'turn_off', mode=mode)
    
    # ── Hardware Abstraction ──
    try:
        from hardware import hardware_control
        hardware_control(device, on)
    except Exception as hw_err:
        print(f'[HW Error] {hw_err}')

    return {'success': True, 'device': device, 'state': state[device]}

def apply_ai_decisions(decisions: dict):
    """Apply AI decisions to all devices via set_device"""
    changed = []
    for device, decision in decisions.items():
        res = set_device(device, decision.get('on', False), mode='auto', **{
            k: v for k, v in decision.items() if k != 'on'
        })
        if res.get('success'):
            changed.append(device)
    return changed

def get_all():
    return _load()

# set_mode removed as per-device mode is deprecated for system-wide mode.
