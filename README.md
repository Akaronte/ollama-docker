```markdown
# Repositorio de Modelos de IA en Contenedores Docker con GPU

Este repositorio tiene como objetivo centralizar y facilitar la ejecución de modelos de Inteligencia Artificial (IA) dentro de contenedores Docker. Cada contenedor está configurado para utilizar la GPU (Unidad de Procesamiento Gráfico) para acelerar significativamente el rendimiento de los modelos, especialmente aquellos grandes y complejos. Esto permite una inferencia más rápida y eficiente en comparación con el uso exclusivo de la CPU.

## Requisitos

* **Docker:** Asegúrate de tener Docker instalado en tu sistema. Puedes encontrar las instrucciones de instalación aquí: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
* **NVIDIA Container Toolkit:** Este toolkit es esencial para permitir que los contenedores Docker accedan a la GPU. Puedes encontrar las instrucciones de instalación aquí: [https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
* **Suficiente Memoria GPU:** La cantidad de memoria GPU necesaria variará dependiendo del tamaño de los modelos que intentes ejecutar. Asegúrate de tener suficiente memoria para evitar errores de falta de memoria.
* **Ollama (Opcional, pero recomendado):** Este repositorio asume que se utiliza Ollama para gestionar los modelos. Ollama simplifica la descarga, ejecución y gestión de modelos de IA. Instalación aquí: [https://ollama.com/](https://ollama.com/)

## Estructura del Repositorio

Aunque este es un repositorio de ejemplos, se asume una estructura básica donde cada modelo a ejecutar (por ejemplo, `deepseek-r1`, `gemma3`, `llama2`) podría tener su propia carpeta (opcional) con archivos de configuración o scripts específicos. En la práctica, los modelos se descargarán y gestionarán directamente con Ollama.

## Comandos de Ejemplo (Usando Ollama)

Los siguientes comandos ilustran cómo puedes interactuar con los contenedores Docker y ejecutar modelos usando Ollama:

1. **Acceder al Shell del Contenedor:**

   ```bash
   docker exec -ti ollama bash
   ```

   Esto te permite acceder a un shell interactivo dentro del contenedor `ollama`. Esto es útil para inspeccionar el contenedor, solucionar problemas o ejecutar comandos directamente dentro del entorno. El nombre del contenedor puede variar según la configuración.

2. **Descargar un Modelo:**

   ```bash
   ollama pull deepseek-r1
   ```

   Este comando descarga el modelo `deepseek-r1` usando Ollama. El modelo se almacenará en el contenedor.

3. **Ejecutar un Modelo con Verbose Mode:**

   ```bash
   ollama run deepseek-r1:7b --verbose
   ```

   Este comando ejecuta el modelo `deepseek-r1` con la variante 7b y habilita el modo verbose, que muestra más información sobre el proceso de inferencia.

4. **Ejecutar un Modelo (Ejemplo más simple):**

   ```bash
   ollama run gemma3:4b
   ```

   Este comando ejecuta el modelo `gemma3` con la variante 4b.

5. **Ejecutar un Modelo (Ejemplo con parámetro):**

   ```bash
   ollama run llama2:70b --prompt "Escribe un poema sobre la naturaleza"
   ```

   Este comando ejecuta el modelo `llama2` con la variante 70b y le pasa un prompt.

## Notas Importantes

* **Nombres de contenedores:** Asegúrate de que el nombre del contenedor en los comandos (ej., `ollama`) coincida con el nombre del contenedor que estás utilizando.
* **Verificación de la GPU:** Después de ejecutar los comandos, verifica que la GPU se esté utilizando correctamente. Puedes usar herramientas como `nvidia-smi` dentro del contenedor para confirmar.
* **Uso de memoria:** Monitorea el uso de la memoria de la GPU. Los modelos grandes pueden requerir mucha memoria.
* **Optimización:** Experimenta con diferentes parámetros y configuraciones de Ollama para optimizar el rendimiento del modelo.
* **Ollama Configuration:** Considera configurar Ollama a través de archivos .env para gestionar los parámetros y la configuración.

## Contribución

Si tienes modelos de IA que quieres agregar a este repositorio o si tienes ideas para mejorar la configuración, ¡no dudes en contribuir! Crea un fork del repositorio, haz tus cambios y crea un pull request.


DESCARGAR MODELOS DENTRO DEL CONTENEDOR OLLAMA DE:
https://ollama.com/search