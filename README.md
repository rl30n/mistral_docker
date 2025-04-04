# 🧠 Mistral + Elastic Stack Demo

Este proyecto contiene un entorno completo de contenedores Docker que integra:

- Un modelo de lenguaje local (`ai/mistral`) compatible con la API de OpenAI.
- Un stack completo de observabilidad con Elasticsearch, Kibana y Enterprise Search.
- Una aplicación web personalizada que consulta Elasticsearch y genera respuestas con Mistral.

---
## Supuestos

El elasticsearch estará vacío por defecto y con el uso de elasticdump hay que cargar el template y los datos de la carpeta example-info

___

## 📦 Servicios incluidos

| Servicio        | Descripción                                                                 |
|----------------|------------------------------------------------------------------------------|
| `mistral`       | Contenedor con el modelo de lenguaje `openchat` accesible vía `/v1/chat/completions`. |
| `app`           | Aplicación web en Python que permite hacer preguntas a las FAQs de Repsol. |
| `es01`          | Nodo principal de Elasticsearch con certificados y autenticación.          |
| `kibana`        | Interfaz de visualización para Elasticsearch.                              |
| `enterprisesearch` | API de búsqueda empresarial y gestión de contenido.                   |
| `setup`         | Inicializa los certificados SSL y credenciales necesarias.                 |

---

## 🚀 Cómo usar

### 1. Requisitos previos

- Docker + Docker Compose instalados.
- Sistema operativo: **Linux x86_64**.
- Un archivo `.env` con estas variables definidas:

```env
STACK_VERSION=8.15.1
ELASTIC_PASSWORD=changeme
KIBANA_PASSWORD=changeme
CLUSTER_NAME=es-cluster
LICENSE=basic
MEM_LIMIT=4294967296
ES_PORT=9200
KIBANA_PORT=5601
ENTERPRISE_SEARCH_PORT=3002
ENCRYPTION_KEYS=supersecretkey
```

---

### 2. Clonar el repositorio y construir

```bash
git clone <este-repo>
cd mistral-container
docker compose --env-file .env up --build
```

Este comando:

- Construirá la aplicación `app` desde su `Dockerfile`.
- Descargará las imágenes necesarias (`elasticsearch`, `kibana`, `enterprise-search`, `ai/mistral`).
- Inicializará los certificados y contraseñas.
- Levantará todos los servicios en red compartida.

---

### 3. Acceso a los servicios

| Servicio | URL                                       |
|----------|-------------------------------------------|
| App      | http://localhost:8000                     |
| Kibana   | http://localhost:5601                     |
| Enterprise Search | http://localhost:3002           |
| Mistral API | http://localhost:11434/v1/chat/completions |

---

### 4. Funcionalidad principal

La aplicación web:

- Toma una pregunta del usuario sobre las FAQs de Repsol.
- Busca información relevante en un índice de Elasticsearch.
- Genera una respuesta enriquecida utilizando el modelo de Mistral (OpenChat).
- Devuelve el resultado en una interfaz web simple.

---

### 5. Test rápido del modelo Mistral vía `curl`

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openchat",
    "messages": [
      {"role": "user", "content": "¿Qué es Repsol?"}
    ]
  }'
```

---

### 6. Para detener y limpiar

```bash
docker compose down -v
```

Esto detiene los contenedores y elimina los volúmenes persistentes.

---

### 📝 Notas adicionales

- La red usada se llama `mistral-net` y permite que todos los contenedores se resuelvan por nombre.
- Los certificados se generan automáticamente en el contenedor `setup` y se comparten entre servicios.
- El modelo de lenguaje se sirve directamente sin necesidad de `ollama`.

---

### ⚠️ Compatibilidad

- Este entorno **no funciona en Apple Silicon (M1/M2/M3)** sin emulación (QEMU).
- Está diseñado y probado para entornos **Linux x86_64**.
- Para Mac, se recomienda usar `ollama/ollama` como alternativa.