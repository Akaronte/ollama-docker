import base64
import requests
from PIL import ImageGrab
import io
import os

# Configura tu API key aquí
API_KEY = ""
API_URL = "https://api.openai.com/v1/chat/completions"

# Captura de pantalla (funciona en Windows, macOS y Linux con entorno gráfico)
screenshot = ImageGrab.grab()
buffered = io.BytesIO()
screenshot.save(buffered, format="PNG")
base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

# Prepara el contenido de la solicitud
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

prompt = "Describe detalladamente lo que ves en esta captura de pantalla."

data = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 500
}

# Envía la solicitud
response = requests.post(API_URL, headers=headers, json=data)

# Muestra la respuesta
if response.status_code == 200:
    result = response.json()
    reply = result['choices'][0]['message']['content']
    print("\n🧠 Respuesta de GPT-4 Vision:")
    print(reply)
else:
    print(f"❌ Error {response.status_code}: {response.text}")
