# Historia

Análisis de Shorts de YouTube de historia para crear contenido similar.

## Canal de referencia
- [@cdmauro2010](https://www.youtube.com/@cdmauro2010/shorts)

## Estructura
```
prompts/      # Prompts para los agentes de análisis (Gemini 4 Argon)
analisis/     # Informes generados por los agentes
data/raw/     # Vídeos, frames y metadatos descargados (ignorado por git)
```

## Flujo
1. Ejecutar el prompt [`prompts/01_analisis_canal_cdmauro2010.md`](prompts/01_analisis_canal_cdmauro2010.md) con Gemini 4 Argon.
2. Los resultados se guardan en `analisis/cdmauro2010/`.
3. Usar el kit de producción y las ideas generadas para crear nuestros Shorts.
