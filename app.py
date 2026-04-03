from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import os
from datetime import datetime

# SQLite database (replaces Google Sheets — fully offline)
from database import (
    init_db, insert_sensor, get_sensor_history,
    insert_device_log, get_device_logs,
    insert_ai_log, get_ai_logs,
    insert_irrigation_log, get_irrigation_logs,
    insert_alert, get_active_alerts, resolve_alert, resolve_alerts_by_type, get_alert_summary
)
init_db()


# Import AI disease detection (optional - will use demo mode if not available)
try:
    from ai_disease_model import predict_disease
    AI_MODEL_AVAILABLE = True
    print("✅ AI Disease Detection Model loaded")
except Exception as e:
    AI_MODEL_AVAILABLE = False
    print(f"⚠️  AI Model not available: {str(e)}")
    print("   Using demo mode for disease detection")

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'krishishakti-secret-key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Google Sheets removed — using SQLite (see database.py)

# Track last received sensor data for dynamic connection status
last_hardware_update = None

# Store sensor data
sensor_data = {
    'mq135': {'value': None, 'unit': 'ppm', 'name': 'Air Quality (MQ-135)'},
    'pms5003': {'pm25': None, 'pm10': None, 'unit': 'µg/m³', 'name': 'Particulate Matter (PMS5003)'},
    'dht22': {'temperature': None, 'humidity': None, 'name': 'Temperature & Humidity (DHT22)'},
    'fc28': {'value': None, 'unit': '%', 'name': 'Water Tank Level (FC-28)'},
    'tds': {'value': None, 'unit': 'ppm', 'name': 'Water Quality (TDS Sensor)'},
    'location': None,
    'timestamp': datetime.now().isoformat()
}

# Data directory
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Legacy JSON history removed — using SQLite (see database.py)

# Routes
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # Never intercept API routes — let Flask handle them
    if path.startswith('api/'):
        from flask import abort
        abort(404)
    return send_from_directory('public', path)

@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    global sensor_data
    # Include dynamic connection status in the response
    status_info = get_arduino_status_logic()
    
    # Check if data is stale (Treat as None if older than 30 seconds)
    stale = False
    if last_hardware_update:
        diff = (datetime.now() - last_hardware_update).total_seconds()
        if diff > 30:
            stale = True
    else:
        stale = True

    response = sensor_data.copy()
    
    if stale:
        # Mark all sensors as None if hardware is disconnected
        response['mq135']['value'] = None
        response['pms5003']['pm25'] = None
        response['pms5003']['pm10'] = None
        response['dht22']['temperature'] = None
        response['dht22']['humidity'] = None
        response['fc28']['value'] = None
        response['tds']['value'] = None
    
    response['arduino_status'] = status_info['status']
    response['arduino_color'] = status_info['color']
    return jsonify(response)

@app.route('/api/sensors', methods=['POST'])
def update_sensors():
    global sensor_data, last_hardware_update
    data = request.json
    
    # Track heartbeat
    last_hardware_update = datetime.now()
    
    # Sanity checks and validation logic
    def validate(val, min_v, max_v, name='sensor'):
        try:
            if val is None: return None
            v = float(val)
            
            # HARD REJECTION: Exactly 0.0 for certain sensors often means "not connected"
            if name in ['temperature', 'humidity', 'mq135'] and v == 0.0:
                return None
                
            if min_v <= v <= max_v: return v
            return None
        except: return None

    sensor_data = {
        'mq135': {'value': validate(data.get('mq135'), 5, 1000, 'mq135'), 'unit': 'ppm', 'name': 'Air Quality (MQ-135)'},
        'pms5003': {
            'pm25': validate(data.get('pm25'), 0, 500, 'pm25'), 
            'pm10': validate(data.get('pm10'), 0, 500, 'pm10'), 
            'unit': 'µg/m³', 'name': 'Particulate Matter (PMS5003)'
        },
        'dht22': {
            'temperature': validate(data.get('temperature'), -10, 60, 'temperature'), 
            'humidity': validate(data.get('humidity'), 1, 100, 'humidity'), 
            'name': 'Temperature & Humidity (DHT22)'
        },
        'fc28': {'value': validate(data.get('fc28'), 0, 100, 'fc28'), 'unit': '%', 'name': 'Water Tank Level (FC-28)'},
        'tds': {'value': validate(data.get('tds'), 0, 1000, 'tds'), 'unit': 'ppm', 'name': 'Water Quality (TDS Sensor)'},
        'location': data.get('location'),
        'timestamp': datetime.now().isoformat()
    }
    
    # Compute validity: Essential readings must be present
    # Humidity is excluded from the strict check to accommodate Blynk hardware profiles
    essential_sensors = [
        sensor_data['mq135'].get('value'),
        sensor_data['dht22'].get('temperature'),
        sensor_data['fc28'].get('value')
    ]
    is_valid = all([v is not None for v in essential_sensors])
    sensor_data['is_valid'] = 1 if is_valid else 0
    
    # Only save and process if at least one critical sensor has valid data
    if any(sensor_data[k].get('value') is not None for k in ['mq135', 'fc28', 'tds']) or \
       sensor_data['dht22']['temperature'] is not None:
        insert_sensor(sensor_data)
        check_sensor_thresholds(sensor_data)

    # Broadcast to WebSocket clients
    try:
        socketio.emit('sensor_update', sensor_data, to=None)
    except: pass
    
    return jsonify({'success': True, 'data': sensor_data})

@app.route('/api/history', methods=['GET'])
def get_history():
    limit = int(request.args.get('limit', 100))
    hours = int(request.args.get('hours', 24))
    return jsonify(get_sensor_history(limit, hours))

@app.route('/api/sheets/data', methods=['GET'])
def get_sheets_data():
    # Alias kept for frontend compatibility — reads from SQLite
    limit = int(request.args.get('limit', 20))
    hours = int(request.args.get('hours', 24))
    return jsonify(get_sensor_history(limit, hours))

@app.route('/api/logs/devices', methods=['GET'])
def api_device_logs():
    limit = int(request.args.get('limit', 50))
    return jsonify(get_device_logs(limit))

@app.route('/api/logs/ai', methods=['GET'])
def api_ai_logs():
    limit = int(request.args.get('limit', 20))
    return jsonify(get_ai_logs(limit))

@app.route('/api/logs/irrigation', methods=['GET'])
def api_irrigation_logs():
    limit = int(request.args.get('limit', 50))
    return jsonify(get_irrigation_logs(limit))

# ── Connection Status Logic ───────────────────────────────────────────────────
def get_arduino_status_logic():
    """Returns dynamic status based on heartbeat"""
    if last_hardware_update is None:
        return {'status': 'Not Connected', 'color': 'gray'}
    
    diff = (datetime.now() - last_hardware_update).total_seconds()
    if diff > 15:
        return {'status': 'Disconnected', 'color': 'red'}
    
    return {'status': 'Connected', 'color': 'green'}

@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    """Public endpoint for hardware connection state"""
    return jsonify(get_arduino_status_logic())

# ── Alert Endpoints ───────────────────────────────────────────────────────────
@app.route('/api/alerts', methods=['GET'])
def api_get_alerts():
    """Fetch all active system alerts and a summary of counts."""
    return jsonify({
        'alerts': get_active_alerts(),
        'summary': get_alert_summary()
    })

@app.route('/api/alerts/resolve', methods=['POST'])
def api_resolve_alert():
    """Manually resolve a specific alert by ID."""
    data = request.json
    alert_id = data.get('id')
    if alert_id:
        resolve_alert(alert_id)
        socketio.emit('alert_update', {'resolved': alert_id})
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Missing alert ID'}), 400

def check_sensor_thresholds(data):
    """
    Analyzes live sensor data against safety thresholds.
    Generates new alerts or auto-clears existing ones.
    """
    # 1. Air Quality (MQ-135)
    aq_val = data.get('mq135', {}).get('value')
    if aq_val is not None:
        aq_type = 'mq135'
        if aq_val > 200:
            _trigger_alert(aq_type, 'critical', 'Critical: High Air Pollution', f'AQI is dangerously high at {aq_val} ppm.')
        elif aq_val > 100:
            _trigger_alert(aq_type, 'warning', 'Warning: Poor Air Quality', f'AQI is elevated at {aq_val} ppm.')
        else:
            resolve_alerts_by_type(aq_type)

    # 2. Soil Moisture (FC-28 / TDS context)
    moisture = data.get('fc28', {}).get('value')
    if moisture is not None:
        m_type = 'moisture'
        if moisture < 30:
            _trigger_alert(m_type, 'critical', 'Critical: Soil Too Dry', f'Soil moisture is below threshold at {moisture:.1f}%.')
        elif moisture > 85:
            _trigger_alert(m_type, 'warning', 'Warning: Soil Waterlogged', f'Excessive moisture detected ({moisture:.1f}%).')
        else:
            resolve_alerts_by_type(m_type)

    # 3. Water Tank (FC-28 Level)
    tank = data.get('fc28', {}).get('value')
    if tank is not None:
        t_type = 'tank'
        if tank < 10:
            _trigger_alert(t_type, 'critical', 'Critical: Water Tank Low', 'Water generation tank is nearly empty.')
        elif tank > 90:
            _trigger_alert(t_type, 'warning', 'Warning: Tank Nearly Full', 'Water tank is at 90% capacity.')
        else:
            resolve_alerts_by_type(t_type)

    # 4. Water Quality (TDS)
    tds = data.get('tds', {}).get('value')
    if tds is not None:
        tds_type = 'tds'
        if tds > 500:
            _trigger_alert(tds_type, 'warning', 'Warning: Poor Water Quality', f'TDS levels are elevated at {tds} ppm.')
        else:
            resolve_alerts_by_type(tds_type)

def _trigger_alert(alert_type, severity, title, message):
    """Internal helper to insert alert if not already active."""
    active = get_active_alerts()
    # If an alert of this type is already active, don't duplicate (unless severity changed)
    # Simple implementation: resolve existing of same type first
    resolve_alerts_by_type(alert_type)
    insert_alert(alert_type, severity, title, message)
    socketio.emit('new_alert', {'type': alert_type, 'severity': severity, 'title': title})

# AI Disease Prediction Endpoint
@app.route('/api/predict-disease', methods=['POST'])
def predict_disease_api():
    """
    AI-powered crop disease prediction from uploaded image
    Accepts: multipart/form-data with 'image' file
    Returns: JSON with disease prediction and recommendations
    """
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided',
                'message': 'Please upload an image file'
            }), 400
        
        file = request.files['image']
        
        # Check if file is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Empty filename',
                'message': 'Please select a valid image file'
            }), 400
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            return jsonify({
                'success': False,
                'error': 'Invalid file type',
                'message': f'Please upload an image file ({", ".join(allowed_extensions)})'
            }), 400
        
        # Use AI model if available
        if AI_MODEL_AVAILABLE:
            try:
                # Save file temporarily
                temp_path = os.path.join(DATA_DIR, 'temp_crop_image.jpg')
                file.save(temp_path)
                
                # Reset file pointer for model processing
                with open(temp_path, 'rb') as img_file:
                    result = predict_disease(img_file)
                
                # Clean up temp file
                try: os.remove(temp_path)
                except: pass
                
                return jsonify(result)
            except Exception as e:
                return jsonify({'success': False, 'error': f'AI processing failed: {str(e)}'})
        else:
            return jsonify({'success': False, 'error': 'AI disease detection unavailable. Check server logs.'})
            
    except Exception as e:
        print(f"Error in disease prediction: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error processing image.'
        }), 500

@app.route('/api/sheets/setup', methods=['POST'])
def setup_sheets():
    return jsonify({'success': False, 'message': 'Google Sheets interface removed. Using local SQLite.'})

# ChatGPT Chatbot endpoint
@app.route('/api/chatbot/message', methods=['POST'])
def chatbot_message():
    """Handle chatbot messages - AI-powered with Gemini API + Fallback to demo mode"""
    try:
        data = request.json
        user_message = data.get('message', '')
        sensor_data = data.get('sensorData', {})
        history = data.get('history', [])
        
        # Try AI-powered response first
        try:
            from ai_chat import ask_ai
            ai_response = ask_ai(user_message, sensor_data)
            return jsonify({'response': ai_response, 'mode': 'ai'})
        except Exception as ai_error:
            print(f'AI Chatbot Error: {str(ai_error)}')
            return jsonify({'response': '📡 AI service currently unavailable. Please check your data connection and Gemini API key.', 'mode': 'error'})
            
    except Exception as e:
        print(f'Chatbot error: {str(e)}')
        import traceback
        traceback.print_exc()
        # Even on error, return a helpful response in multiple languages
        return jsonify({
            'response': '🌾 I\'m here to help! / मैं मदद के लिए यहाँ हूँ! / ਮੈਂ ਮਦਦ ਲਈ ਇੱਥੇ ਹਾਂ!\n\nAsk me about farming in English, Hindi, or Punjabi!'
        })

# Agriculture AI endpoints
# ─── NEW: AI Engine + Device Controller ──────────────────────────────────────
from ai_engine import ai_decision, log_irrigation, get_irrigation_history
import device_controller as dc
import automation as auto_engine


# ── Start background automation loop ─────────────────────────────────────────
def _broadcast(data):
    try:
        socketio.emit('ai_update', data, to=None)
        if 'devices' in data:
            socketio.emit('device_update', data['devices'], to=None)
    except Exception:
        pass

auto_engine.start_loop(
    get_sensors_fn=lambda: sensor_data,
    apply_fn=dc.apply_ai_decisions,
    broadcast_fn=_broadcast
)

@app.route('/api/ai-decision', methods=['GET', 'POST'])
def get_ai_decision():
    """Run AI decision engine on current sensor data"""
    try:
        moisture = sensor_data.get('fc28',  {}).get('value')
        temp     = sensor_data.get('dht22', {}).get('temperature')
        humidity = sensor_data.get('dht22', {}).get('humidity')
        tank     = sensor_data.get('fc28',  {}).get('value')
        result   = ai_decision(moisture, temp, humidity, tank_level=tank)
        dc.apply_ai_decisions(result['decisions'])
        
        # Log AI decision to SQLite
        try:
            insert_ai_log(result)
        except Exception as db_err:
            print(f'[DB] Manual AI log error: {db_err}')

        socketio.emit('device_update', dc.get_all(), to=None)
        return jsonify(result)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/device-status', methods=['GET'])
def device_status():
    """Simple flat device status for frontend polling"""
    devices = dc.get_all()
    return jsonify({
        dev: ('on' if state.get('on') else 'off')
        for dev, state in devices.items()
    })

@app.route('/api/control-device', methods=['POST'])
def control_device():
    """Manual device control: {device, on, mode}"""
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({'success': False, 'error': 'Invalid JSON body'}), 400

        device = data.get('device')
        on     = bool(data.get('on', False))
        mode   = data.get('mode', 'manual')

        valid_devices = ('pump', 'fan', 'heater')
        if device not in valid_devices:
            return jsonify({'success': False, 'error': f'Unknown device: {device}. Valid: {valid_devices}'}), 400

        extra  = {k: v for k, v in data.items() if k not in ('device', 'on', 'mode')}
        result = dc.set_device(device, on, mode, **extra)

        if result.get('success'):
            socketio.emit('device_update', dc.get_all(), to=None)
            if device == 'pump' and on:
                log_irrigation({'action': 'start', 'mode': mode,
                                'moisture': sensor_data.get('fc28', {}).get('value', 0),
                                'duration_min': data.get('duration_min', 0)})
            elif device == 'pump' and not on:
                log_irrigation({'action': 'stop', 'mode': mode})

        return jsonify(result)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/devices', methods=['GET'])
def get_devices():
    return jsonify(dc.get_all())

# Individual device mode route removed as per-device control is deprecated.

@app.route('/api/irrigation/history', methods=['GET'])
def irrigation_history():
    limit = int(request.args.get('limit', 50))
    return jsonify(get_irrigation_history(limit))


# ─── System mode routes ───────────────────────────────────────────────────────
@app.route('/api/system/mode', methods=['GET'])
def get_mode():
    return jsonify({'mode': auto_engine.get_system_mode()})

@app.route('/api/system/mode', methods=['POST'])
def set_mode():
    data = request.get_json(force=True, silent=True) or {}
    mode = data.get('mode', 'auto')
    if mode not in ('auto', 'manual'):
        return jsonify({'success': False, 'error': 'mode must be auto or manual'}), 400
    result = auto_engine.set_system_mode(mode)
    auto_engine.log_activity(f'🔄 System switched to {mode.upper()} mode', 'system')
    socketio.emit('mode_update', {'mode': mode}, to=None)
    return jsonify({'success': True, **result})

@app.route('/api/activity', methods=['GET'])
def activity_log():
    limit = int(request.args.get('limit', 20))
    return jsonify(auto_engine.get_activity_log(limit))

# WebSocket events
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('sensor_update', sensor_data)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    print('╔════════════════════════════════════════════════════════╗')
    print('║  KrishiShakti - Flask Server                          ║')
    print('║  Smart Agriculture & IoT Monitoring System            ║')
    print('╚════════════════════════════════════════════════════════╝')

    print('\n🌐 Server running on http://localhost:5000')
    print('📊 Dashboard: http://localhost:5000/dashboard.html')
    print('🔔 Press Ctrl+C to stop\n')
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)

