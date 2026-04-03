"""
KrishiShakti Automation Engine
Background control loop — runs AI every N seconds in Auto mode,
applies decisions, enforces stability rules, logs activity.
"""
import threading
import time
import json
import os
import random
from datetime import datetime, timedelta

# ─── System mode ──────────────────────────────────────────────────────────────
_MODE_FILE = os.path.join('data', 'system_mode.json')

def get_system_mode() -> str:
    """Returns 'auto' or 'manual'"""
    try:
        if os.path.exists(_MODE_FILE):
            with open(_MODE_FILE) as f:
                return json.load(f).get('mode', 'auto')
    except Exception:
        pass
    return 'auto'

def set_system_mode(mode: str) -> dict:
    os.makedirs('data', exist_ok=True)
    data = {'mode': mode, 'changed_at': datetime.now().isoformat()}
    with open(_MODE_FILE, 'w') as f:
        json.dump(data, f)
    return data

# ─── Activity log ─────────────────────────────────────────────────────────────
_ACTIVITY_FILE = os.path.join('data', 'activity_log.json')
_MAX_ACTIVITY  = 100

def log_activity(message: str, category: str = 'ai'):
    """Append a human-readable activity entry."""
    try:
        logs = _load_activity()
        logs.append({
            'message':   message,
            'category':  category,
            'timestamp': datetime.now().isoformat()
        })
        os.makedirs('data', exist_ok=True)
        with open(_ACTIVITY_FILE, 'w') as f:
            json.dump(logs[-_MAX_ACTIVITY:], f, indent=2)
    except Exception as e:
        print(f'[Activity log error] {e}')

def get_activity_log(limit: int = 20) -> list:
    return list(reversed(_load_activity()[-limit:]))

def _load_activity() -> list:
    if os.path.exists(_ACTIVITY_FILE):
        try:
            with open(_ACTIVITY_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []

# ─── Stability / anti-flicker ─────────────────────────────────────────────────
# Tracks last time each device changed state to prevent rapid toggling
_last_change: dict = {}          # device -> datetime
_MIN_RUNTIME   = timedelta(seconds=30)   # device must stay ON at least 30s
_MIN_COOLDOWN  = timedelta(seconds=20)   # device must stay OFF at least 20s

def _can_change(device: str, new_state: bool, current_state: bool) -> bool:
    """Returns True if enough time has passed since last state change."""
    if new_state == current_state:
        return False   # no change needed
    last = _last_change.get(device)
    if last is None:
        return True
    elapsed = datetime.now() - last
    if current_state and elapsed < _MIN_RUNTIME:
        return False   # was ON, hasn't run long enough
    if not current_state and elapsed < _MIN_COOLDOWN:
        return False   # was OFF, cooldown not done
    return True

def _record_change(device: str):
    _last_change[device] = datetime.now()

# ─── Control loop ─────────────────────────────────────────────────────────────
_loop_thread: threading.Thread | None = None
_loop_running = False
_LOOP_INTERVAL = 8   # seconds between AI cycles

def start_loop(get_sensors_fn, apply_fn, broadcast_fn):
    """
    Start the background automation loop.
    get_sensors_fn() -> current sensor_data dict
    apply_fn(decisions)  -> apply AI decisions to devices
    broadcast_fn(data)   -> emit WebSocket update
    """
    global _loop_thread, _loop_running
    if _loop_running:
        return
    _loop_running = True

    def _loop():
        from ai_engine import ai_decision, HARDWARE
        import device_controller as dc

        print('[Automation] Control loop started')
        log_activity('🚀 Automation loop started', 'system')

        while _loop_running:
            try:
                mode = get_system_mode()
                if mode != 'auto':
                    time.sleep(_LOOP_INTERVAL)
                    continue

                # Get sensor data
                sensors = get_sensors_fn()
                moisture    = sensors.get('fc28',  {}).get('value', 0)
                temperature = sensors.get('dht22', {}).get('temperature', 0)
                humidity    = sensors.get('dht22', {}).get('humidity', 0)
                tank_level  = sensors.get('fc28',  {}).get('value', 0)

                # Sensor Validation Layer
                if moisture == 0 or temperature == 0:
                    print('[Automation] Waiting for valid sensor data...')
                    # Clear any old AI result in UI
                    broadcast_fn({'type': 'ai_update', 'result': {'valid': False, 'explanation': ['Waiting for real sensor data']}})
                    time.sleep(_LOOP_INTERVAL)
                    continue

                # Run AI
                result = ai_decision(moisture, temperature, humidity, tank_level=tank_level)

                if not result.get('valid'):
                    log_activity('⚠️ Sensor data invalid — AI decisions paused', 'warning')
                    broadcast_fn({'type': 'ai_update', 'result': result})
                    time.sleep(_LOOP_INTERVAL)
                    continue

                # Apply decisions with stability check
                current_devices = dc.get_all()
                decisions       = result.get('decisions', {})
                actions_taken   = []

                for device, decision in decisions.items():
                    if not HARDWARE.get(device):
                        continue
                    dev_state = current_devices.get(device, {})
                    
                    # Strict global mode enforcement:
                    # In AUTO, AI controls everything. Per-device 'mode' is ignored.
                    
                    new_on  = decision.get('on', False)
                    curr_on = dev_state.get('on', False)

                    if not _can_change(device, new_on, curr_on):
                        continue   # stability rule — skip this cycle

                    # Apply
                    dc.set_device(device, new_on, mode='auto', **{
                        k: v for k, v in decision.items() if k != 'on'
                    })
                    _record_change(device)

                    if new_on != curr_on:
                        action_word = 'ON' if new_on else 'OFF'
                        reason = next(
                            (r for r in result.get('explanation', [])
                             if device in r.lower()),
                            'AI decision'
                        )
                        msg = f'🤖 AI turned {device} {action_word} — {reason}'
                        actions_taken.append(msg)
                        log_activity(msg, 'ai')

                        # Log irrigation events only on transitions
                        if device == 'pump':
                            from ai_engine import log_irrigation
                            log_irrigation({
                                'action':       'start' if new_on else 'stop',
                                'mode':         'auto',
                                'moisture':     moisture,
                                'duration_min': decision.get('duration_min', 0)
                            })

                # Log AI decision cycle to SQLite
                try:
                    from database import insert_ai_log
                    insert_ai_log(result)
                except Exception as db_err:
                    print(f'[DB] ai_log write error: {db_err}')

                # Broadcast
                broadcast_fn({
                    'type':         'ai_update',
                    'result':       result,
                    'actions_taken': actions_taken,
                    'devices':      dc.get_all(),
                })

            except Exception as e:
                import traceback
                print(f'[Automation loop error] {e}')
                traceback.print_exc()

            time.sleep(_LOOP_INTERVAL)

        print('[Automation] Control loop stopped')
        log_activity('⏹️ Automation loop stopped', 'system')

    _loop_thread = threading.Thread(target=_loop, daemon=True, name='AutomationLoop')
    _loop_thread.start()

def stop_loop():
    global _loop_running
    _loop_running = False
