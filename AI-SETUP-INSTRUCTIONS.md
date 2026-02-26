# 🤖 AI Chatbot Setup Instructions

## What Changed?

Your chatbot now uses **Google Gemini AI** for intelligent, context-aware responses based on your real sensor data!

### Architecture:
```
Farmer → Website → Flask → Gemini AI → Smart Reply
                              ↑
                    Real Sensor Data
```

## Step 1: Get Your Free Gemini API Key

1. Go to: **https://aistudio.google.com/app/apikey**
2. Login with your Gmail account
3. Click **"Create API Key"**
4. Copy the key (looks like: `AIzaSyD9v...`)
5. Keep it secret!

## Step 2: Add Your API Key

Open `ai_chat.py` and replace this line:

```python
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

With your actual key:

```python
API_KEY = "AIzaSyD9v..."  # Your real key here
```

## Step 3: Install Dependencies

The Gemini library is already being installed. If you need to install it manually:

```bash
source venv/bin/activate
pip install google-generativeai
```

## Step 4: Run Your Server

```bash
source venv/bin/activate
python app.py
```

## Step 5: Test It!

Open: **http://localhost:5001/chatbot.html**

Try these questions:

### English:
- "My soil is dry, what should I do?"
- "Is the air quality good for my crops?"
- "Should I water my plants now?"

### Hindi:
- "मेरी मिट्टी सूखी है क्या करूँ?"
- "मेरे पौधों की पत्तियां पीली हो रही हैं"

### Punjabi:
- "ਮੇਰੀ ਮਿੱਟੀ ਸੁੱਕੀ ਹੈ ਕੀ ਕਰਾਂ?"

## How It Works

1. **Farmer asks question** in any language
2. **System sends**:
   - Question
   - Real sensor data (temperature, humidity, soil moisture, air quality)
3. **Gemini AI analyzes** and gives advice
4. **Response comes back** in the same language

## Fallback Mode

If AI fails (no API key, network issue), the system automatically falls back to your original demo chatbot. Nothing breaks!

## What Makes This Special for Viva?

✅ **Real sensor integration** - AI uses actual telemetry data  
✅ **Multi-language support** - Hindi, Punjabi, English auto-detected  
✅ **Context-aware** - Advice based on current conditions  
✅ **Practical** - Actionable farming recommendations  
✅ **Robust** - Fallback to demo mode if AI unavailable  

## Viva Talking Points

"Our chatbot uses Google Gemini AI to provide context-aware agricultural advice based on real-time sensor telemetry. The AI analyzes current temperature, humidity, soil moisture, and air quality to give farmers actionable recommendations in their native language."

## Troubleshooting

### Error: "AI Error: API key not valid"
→ Check your API key in `ai_chat.py`

### Error: "Module not found: google.generativeai"
→ Run: `pip install google-generativeai`

### Chatbot still works but says "demo mode"
→ AI is not configured, but fallback is working (this is good!)

## Files Modified

- ✅ `ai_chat.py` - NEW: AI integration module
- ✅ `app.py` - MODIFIED: Chatbot endpoint now uses AI
- ✅ All existing functionality preserved

## Next Steps

1. Get your API key
2. Add it to `ai_chat.py`
3. Test with real questions
4. Prepare for viva! 🎓
