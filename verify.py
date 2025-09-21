import openai
import os

def verificar_token(api_key):
    try:
        # Configura la clave API
        openai.api_key = api_key
        
        # Prueba haciendo una solicitud para obtener tu balance de tokens (un endpoint simple y rápido)
        response = openai.Model.list()
        
        # Si llegamos aquí, el token es válido
        print("El token es válido.")
        print(f"Modelos disponibles: {[model['id'] for model in response['data']]}")
        
    except openai.error.AuthenticationError:
        print("El token no es válido. Por favor verifica tu clave de API.")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")

if __name__ == "__main__":
    # Puedes reemplazar esto con tu clave de API
    token = os.getenv("OPENAI_API_KEY", "tu-api-key-aqui")
    verificar_token(token)
