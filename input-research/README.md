# Cliente React para API

Aplicación web sencilla creada con Vite y React que permite enviar texto a un endpoint mediante una petición POST con cuerpo JSON y visualizar la respuesta en la interfaz.

## Requisitos previos

- Node.js 18 o superior
- npm 9 o superior

## Puesta en marcha

```bash
npm install
npm run dev
```

Abrir `http://localhost:5173` en el navegador.

## Configuración del endpoint

El helper `src/api.js` define la constante `ENDPOINT_URL`. Reemplázala con la URL real de tu servicio antes de ejecutar la aplicación en producción.

## Scripts disponibles

- `npm run dev`: inicia el servidor de desarrollo con recarga en caliente.
- `npm run build`: genera la versión optimizada para producción.
- `npm run preview`: sirve en local la build generada.

## Estructura principal

- `src/App.jsx`: componente principal con el formulario y la visualización de resultados.
- `src/api.js`: capa ligera para las llamadas a la API.
- `src/App.module.css`: estilos modulares del componente.
- `src/index.css`: estilos globales mínimos.
