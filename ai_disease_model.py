"""
AI Crop Disease Detection using OpenRouter Vision API
Sends crop image to a vision-capable model for disease analysis
"""

import os
import json
import base64
import urllib.request
import urllib.error
from PIL import Image
import io

OPENROUTER_API_KEY = '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'
OPENROUTER_MODEL   = 'google/gemini-2.0-flash-001'   # vision-capable model


def _encode_image(image_file) -> tuple[str, str]:
    """Read image file, resize if needed, return (base64_str, mime_type)."""
    img = Image.open(image_file).convert("RGB")

    # Resize to max 1024px on longest side to keep payload small
    max_px = 1024
    w, h = img.size
    if max(w, h) > max_px:
        scale = max_px / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return b64, "image/jpeg"


def predict_disease(image_file) -> dict:
    """
    Analyse a crop image with an OpenRouter vision model.

    Args:
        image_file: file-like object or path to image

    Returns:
        dict with keys: success, disease, confidence, is_healthy, recommendations, model_type
    """
    try:
        b64_image, mime_type = _encode_image(image_file)
    except Exception as e:
        return {"success": False, "error": str(e), "message": "Could not read image file."}

    prompt = """You are an expert plant pathologist. Analyse this crop image and respond ONLY with valid JSON (no markdown, no code fences).

JSON schema:
{
  "disease": "<disease name or 'Healthy Plant'>",
  "is_healthy": <true|false>,
  "confidence": <integer 0-100>,
  "description": "<one sentence summary>",
  "recommendations": ["<step 1>", "<step 2>", "<step 3>", "<step 4>", "<step 5>"]
}

Rules:
- If the plant looks healthy set is_healthy=true and disease="Healthy Plant".
- confidence is your certainty percentage.
- recommendations must be practical, actionable steps for an Indian farmer.
- Return ONLY the JSON object, nothing else."""

    payload = json.dumps({
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{b64_image}"}
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type":  "application/json",
            "HTTP-Referer":  "https://krishishakti.local",
            "X-Title":       "KrishiShakti"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
            content = raw["choices"][0]["message"]["content"].strip()

            # Strip markdown fences if model adds them anyway
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            result = json.loads(content)

            return {
                "success":         True,
                "disease":         result.get("disease", "Unknown"),
                "is_healthy":      result.get("is_healthy", False),
                "confidence":      result.get("confidence", 0),
                "description":     result.get("description", ""),
                "recommendations": result.get("recommendations", []),
                "model_type":      f"OpenRouter / {OPENROUTER_MODEL}"
            }

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        return {"success": False, "error": f"API error {e.code}: {body[:300]}",
                "message": "OpenRouter API request failed."}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON parse error: {e}",
                "message": "Model returned unexpected format."}
    except Exception as e:
        return {"success": False, "error": str(e),
                "message": "Disease detection failed. Please try again."}
