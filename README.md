docker exec -ti ollama bash 

ollama pull deepseek-r1

ollama run deepseek-r1:7b --verbose

ollama pull gemma3:4b

ollama run gemma3:4b

ollama run llama2:70b  --verbose