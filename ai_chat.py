"""
AI-powered chatbot using Google Gemini API
Context-aware agricultural advisor based on real sensor telemetry
"""

try:
    # Try new package first
    from google import genai
    from google.genai import types
    USE_NEW_API = True
except ImportError:
    # Fallback to old package
    import google.generativeai as genai
    USE_NEW_API = False

# API Key - Already configured
API_KEY = "AIzaSyCDMswFyUGpw6UP-9fJmjVYq8JESNWvp90"


# Configure Gemini based on which API we're using
if USE_NEW_API:
    client = genai.Client(api_key=API_KEY)
else:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

def ask_ai(user_message, sensor_data):
    """
    Ask Gemini AI for agricultural advice based on sensor data
    
    Args:
        user_message: The farmer's question
        sensor_data: Current sensor readings from the system
    
    Returns:
        AI-generated response in the same language as the question
    """
    
    # Extract sensor values safely
    temperature = sensor_data.get('dht22', {}).get('temperature', 25)
    humidity = sensor_data.get('dht22', {}).get('humidity', 60)
    soil_moisture = sensor_data.get('fc28', {}).get('value', 50)
    air_quality = sensor_data.get('mq135', {}).get('value', 100)
    pm25 = sensor_data.get('pms5003', {}).get('pm25', 15)
    pm10 = sensor_data.get('pms5003', {}).get('pm10', 25)
    
    # Build context with real sensor data
    context = f"""You are an expert agricultural advisor helping farmers in India.

Current Farm Sensor Data (REAL-TIME):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌡️  Temperature: {temperature}°C
💧 Humidity: {humidity}%
🌱 Soil Moisture: {soil_moisture}%
💨 Air Quality (MQ-135): {air_quality} ppm
🌫️  PM2.5: {pm25} µg/m³
🌫️  PM10: {pm10} µg/m³
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTANT INSTRUCTIONS:
1. Give practical, actionable farming advice based on these REAL sensor readings
2. If the farmer asks in Hindi, Punjabi, or any Indian language, reply in the SAME language
3. If the farmer asks in English, reply in English
4. Keep answers concise and farmer-friendly (2-4 sentences)
5. Reference the actual sensor values in your response
6. Focus on immediate actions the farmer can take

Examples:
- If soil moisture is low → suggest irrigation
- If temperature is high → suggest shade/cooling
- If air quality is poor → warn about crop health
- If humidity is high → warn about fungal diseases
"""
    
    # Combine context with user question
    full_prompt = context + "\n\nFarmer's Question: " + user_message
    
    try:
        # Generate response based on API version
        if USE_NEW_API:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=full_prompt
            )
            return response.text
        else:
            response = model.generate_content(full_prompt)
            return response.text
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg or "API key" in error_msg:
            return "⚠️ AI Configuration Error: Please check your API key in ai_chat.py"
        else:
            return f"⚠️ AI Error: {error_msg}"
