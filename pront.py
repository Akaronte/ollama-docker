import base64
import requests
from PIL import ImageGrab
import io
import keyboard  # para detectar teclas

# Configura tu API key aquí
API_KEY = ""
API_URL = "https://api.openai.com/v1/chat/completions"

# Encabezados de la solicitud
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("🔁 Iniciando el modo captura. Escribe un prompt y presiona ENTER.")
print("❌ Pulsa ESC en cualquier momento para salir.\n")

while True:
    # Salir si se pulsa ESC
    if keyboard.is_pressed('esc'):
        print("👋 Saliste del programa.")
        break

    # Introducir el prompt
    prompt = input("📝 Introduce tu prompt: ")

    # Captura de pantalla
    screenshot = ImageGrab.grab()
    buffered = io.BytesIO()
    screenshot.save(buffered, format="PNG")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Cuerpo de la solicitud
    data = {
        "model": "gpt-4o",  # modelo actualizado con visión
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

    # Enviar solicitud
    response = requests.post(API_URL, headers=headers, json=data)

    # Mostrar respuesta
    if response.status_code == 200:
        result = response.json()
        reply = result['choices'][0]['message']['content']
        print("\n🧠 GPT-4o respondió:")
        print(reply)
        print("-" * 60)
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        print("-" * 60)
