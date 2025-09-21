import openai
import os

# Configura tu API Key
openai.api_key = ''

# Prueba de conversación
response = openai.ChatCompletion.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "¿Cuál es la capital de Francia?"}
    ]
)

# Imprime la respuesta del modelo
print(response.choices[0].message.content)
