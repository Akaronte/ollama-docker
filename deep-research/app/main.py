import os
import requests
from typing import List, Optional
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# =======================
# Configuración
# =======================

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://192.168.1.6:11434/api")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:12b")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

if not BRAVE_API_KEY:
    raise RuntimeError("Falta la variable de entorno BRAVE_API_KEY")

BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

app = FastAPI(
    title="Deep Research Agent",
    description="API para investigación profunda usando OpenAI + búsqueda web en tiempo real.",
    version="0.1.0",
)

# Habilitar CORS para todas las solicitudes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================
# Modelos de datos
# =======================

class ResearchRequest(BaseModel):
    query: str = Field(..., description="Tema o pregunta de investigación.")
    depth: int = Field(2, ge=1, le=3, description="Profundidad de investigación (1-3).")

class ResearchSource(BaseModel):
    title: str
    url: str
    snippet: str

class ResearchResponse(BaseModel):
    query: str
    depth: int
    summary: str
    key_points: List[str]
    sources: List[ResearchSource]

# =======================
# Funciones auxiliares
# =======================

def brave_search(query: str, count: int = 5) -> List[ResearchSource]:
    """Hace una búsqueda en Brave Search y devuelve una lista de fuentes básicas."""
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    params = {
        "q": query,
        "count": count,
        "safesearch": "moderate",
        "country": "us",
    }

    resp = requests.get(BRAVE_SEARCH_URL, headers=headers, params=params, timeout=15)
    if resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Error al consultar Brave Search: {resp.status_code} {resp.text}",
        )

    data = resp.json()
    web_results = data.get("web", {}).get("results", [])
    sources: List[ResearchSource] = []

    for item in web_results:
        title = item.get("title", "Sin título")
        url = item.get("url", "")
        snippet = item.get("description", "") or item.get("snippet", "")
        sources.append(ResearchSource(title=title, url=url, snippet=snippet))

    return sources


def build_context_from_sources(sources: List[ResearchSource]) -> str:
    """Crea un texto que resume las fuentes para pasar al modelo."""
    lines = []
    for i, s in enumerate(sources, start=1):
        lines.append(
            f"Fuente {i}:\n"
            f"Título: {s.title}\n"
            f"URL: {s.url}\n"
            f"Resumen/fragmento: {s.snippet}\n"
        )
    return "\n\n".join(lines)


def ask_ollama_for_research(query: str, depth: int, sources: List[ResearchSource]) -> ResearchResponse:
    """Llama al modelo de Ollama para generar un informe de investigación a partir de las fuentes."""
    context_text = build_context_from_sources(sources)

    system_prompt = (
        "Eres un asistente de investigación experto. "
        "Tu tarea es producir un informe claro, con rigor y bien estructurado, "
        "solo usando la información de las fuentes proporcionadas. "
        "Si algo no está en las fuentes, dilo explícitamente."
    )

    depth_explanation = {
        1: "Haz un resumen breve (máx. 3–4 párrafos) y una lista corta de puntos clave.",
        2: "Haz un resumen detallado (5–10 párrafos), puntos clave y conclusiones.",
        3: "Haz un informe extenso y profundo, con contexto histórico, estado actual y posibles controversias.",
    }[depth]

    user_prompt = f"""
Tema de investigación:
\"\"\"{query}\"\"\"

Nivel de profundidad solicitado: {depth}.

Instrucciones:
- Usa exclusivamente la información de las fuentes listadas más abajo.
- Cita las fuentes de forma informal en el texto (por ejemplo: "según la Fuente 2, ...").
- Organiza la respuesta en:
  1) Resumen general,
  2) Puntos clave en viñetas,
  3) Comentarios o matices (si hay contradicciones entre fuentes).

{depth_explanation}

Fuentes:
{context_text}
"""

    # Llamar a Ollama API
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "temperature": 0.4,
    }

    try:
        response = requests.post(
            f"{OLLAMA_API_URL}/chat",
            json=payload,
            timeout=60,
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Error al consultar Ollama: {response.status_code} {response.text}",
            )
        result = response.json()
        content = result.get("message", {}).get("content", "")
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="No se puede conectar al servidor Ollama. Asegúrate de que está ejecutándose.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la respuesta de Ollama: {str(e)}",
        )

    # Separar zonas de la respuesta del modelo:
    # Aquí hacemos un parseo simple; si quieres puedes definir un formato JSON explícito.
    # Para mantenerlo sencillo, intentamos encontrar una sección de puntos clave como líneas con "- ".
    lines = [l.strip() for l in content.splitlines() if l.strip()]

    summary_parts = []
    key_points = []

    in_keypoints = False
    for line in lines:
        if line.lower().startswith("puntos clave") or line.lower().startswith("• puntos clave"):
            in_keypoints = True
            continue
        if in_keypoints and (line.startswith("-") or line.startswith("*")):
            key_points.append(line.lstrip("-* ").strip())
        elif in_keypoints:
            # Salimos de la sección de puntos clave si encontramos otra cosa
            pass
        else:
            summary_parts.append(line)

    summary_text = "\n".join(summary_parts) if summary_parts else content

    return ResearchResponse(
        query=query,
        depth=depth,
        summary=summary_text,
        key_points=key_points,
        sources=sources,
    )


# =======================
# Endpoints
# =======================

@app.post("/research", response_model=ResearchResponse)
def research(req: ResearchRequest):
    """
    Hace investigación profunda sobre un tema usando:
    - Búsqueda web (Brave Search)
    - Modelo de Ollama
    """
    try:
        # Puedes aumentar el número total de resultados según la profundidad
        total_results = {1: 4, 2: 8, 3: 12}[req.depth]
        sources = brave_search(req.query, count=total_results)
        if not sources:
            raise HTTPException(status_code=404, detail="No se encontraron fuentes web relevantes.")

        result = ask_ollama_for_research(req.query, req.depth, sources)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {
        "message": f"Deep Research Agent usando Ollama ({OLLAMA_MODEL}) + Brave Search.",
        "ollama_model": OLLAMA_MODEL,
        "ollama_api_url": OLLAMA_API_URL,
        "usage": "POST /research con JSON {'query': 'tu tema', 'depth': 1-3}",
    }