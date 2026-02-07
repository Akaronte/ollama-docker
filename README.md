# Ollama Docker

This repository contains Docker configurations for running Ollama models in containers.

## Getting Started

### Prerequisites
- Docker installed on your system

### Usage
1. Clone this repository
2. Build the Docker image:
   ```bash
   docker build -t ollama .
   ```
3. Run the container:
   ```bash
   docker run -p 11434:11434 ollama
   ```

## Available Models
- Llama 2
- Mistral
- Gemma

## License
This project is licensed under the MIT License.
