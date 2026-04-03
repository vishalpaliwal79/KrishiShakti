"""
AI-powered chatbot using OpenRouter API
Context-aware agricultural advisor based on real sensor telemetry
"""

import os
import json
import urllib.request
import urllib.error

# OpenRouter API key — set via environment variable or hardcode here
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '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')

# Model to use — change to any OpenRouter-supported model
OPENROUTER_MODEL = os.environ.get('OPENROUTER_MODEL', 'openai/gpt-4o-mini')


def ask_ai(user_message, sensor_data):
    """
    Ask OpenRouter AI for agricultural advice based on sensor data.

    Args:
        user_message: The farmer's question
        sensor_data: Current sensor readings from the system

    Returns:
        AI-generated response string
    """

    # Extract sensor values safely
    temperature   = sensor_data.get('dht22', {}).get('temperature')
    humidity      = sensor_data.get('dht22', {}).get('humidity')
    soil_moisture = sensor_data.get('fc28', {}).get('value')
    air_quality   = sensor_data.get('mq135', {}).get('value')
    pms           = sensor_data.get('pms5003', {})
    pm25          = pms.get('pm25')
    pm10          = pms.get('pm10')

    is_connected = any(v is not None for v in [temperature, soil_moisture, air_quality])
    status_str   = "CONNECTED" if is_connected else "DISCONNECTED / NO DATA"

    location = sensor_data.get('location', {}) or {}
    city     = location.get('city', 'Unknown')
    country  = location.get('country', 'India')

    system_prompt = f"""You are an expert agricultural advisor helping farmers in India.

SYSTEM STATUS: {status_str}

Current Farm Sensor Data (REAL-TIME):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Location: {city}, {country}
🌡️  Temperature: {f'{temperature}°C' if temperature is not None else 'NO DATA'}
💧 Humidity: {f'{humidity}%' if humidity is not None else 'NO DATA'}
🌱 Soil Moisture: {f'{soil_moisture}%' if soil_moisture is not None else 'NO DATA'}
💨 Air Quality (MQ-135): {f'{air_quality} ppm' if air_quality is not None else 'NO DATA'}
🌫️  PM2.5: {f'{pm25} µg/m³' if pm25 is not None else 'NO DATA'}
🌫️  PM10: {f'{pm10} µg/m³' if pm10 is not None else 'NO DATA'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTANT INSTRUCTIONS:
1. If status is "DISCONNECTED / NO DATA", tell the farmer that live sensor readings are unavailable.
2. Provide general advice if data is missing, but prioritize real-time data when available.
3. If the farmer asks in Hindi, Punjabi, or any Indian language, reply in the SAME language.
4. Keep answers concise and farmer-friendly (3-5 sentences).
5. ONLY reference the sensor values shown above. DO NOT make up fake data."""

    payload = json.dumps({
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ]
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        data=payload,
        headers={
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type':  'application/json',
            'HTTP-Referer':  'https://krishishakti.local',
            'X-Title':       'KrishiShakti'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        if e.code == 401:
            raise Exception("OpenRouter API key is invalid or missing.")
        elif e.code == 402:
            raise Exception("OpenRouter account has insufficient credits.")
        else:
            raise Exception(f"OpenRouter API error {e.code}: {body[:200]}")
    except Exception as e:
        raise Exception(f"AI service unavailable: {str(e)}")


if __name__ == '__main__':
    print("KrishiShakti AI Chatbot Test (OpenRouter)\n")

    test_sensor_data = {
        'dht22':   {'temperature': 15.0, 'humidity': 65.0},
        'fc28':    {'value': 45.0},
        'mq135':   {'value': 84.0},
        'pms5003': {'pm25': 35.0, 'pm10': 50.0},
        'location': {'city': 'Landran', 'country': 'India'}
    }

    question = "What should I do about my soil moisture?"
    print(f"Question: {question}\n")

    try:
        response = ask_ai(question, test_sensor_data)
        print(f"Response:\n{response}")
        print("\n✅ OpenRouter chatbot is working!")
    except Exception as e:
        print(f"❌ Error: {e}")
