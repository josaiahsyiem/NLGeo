# NLGeo

**Ask geographic questions in plain English and get interactive maps in seconds.**

NLGeo is a geospatial analysis application that lets users explore OpenStreetMap data using natural language instead of GIS software or SQL. Enter a question such as **"Which Mumbai wards have the highest flood-exposed population?"** or **"How many pharmacies are there in each Berlin district?"**, and NLGeo retrieves the required data, performs the analysis, and generates an interactive choropleth map.

🎥 **[Demo Video](https://youtu.be/h7c9p2f2qqk)**

---

## Features

- Ask geographic questions in plain English
- Interactive choropleth maps
- Live OpenStreetMap data retrieval
- Deterministic spatial analysis with LLM fallback
- Automatic result validation
- Multi-city support
- Population-normalized analysis using WorldPop
- Spatial joins using uploaded files
- CSV and GeoJSON export

---

## Workflow

1. Search vector memory for similar queries.
2. Convert the request into a structured analysis plan.
3. Retrieve administrative boundaries and OpenStreetMap features.
4. Run deterministic GIS analysis whenever possible.
5. Use LLM-generated geospatial code for unsupported queries.
6. Validate the results.
7. Return an interactive map together with the computed metrics.

---

## Results

NLGeo has been tested across **20+ cities** covering flood analysis, healthcare accessibility, greenspace analysis, population-normalized metrics, and spatial joins.

| City | Example Query | Validation | Time |
|------|---------------|-----------:|------:|
| Mumbai | Flood exposure by ward | Spearman = **1.00** | 6–10 s |
| Berlin | Pharmacies by district | Spearman = **1.00** | 33–42 s |
| London | Hospital density | Spearman = **1.00** | 42 s |
| Paris | Restaurants by arrondissement | Spearman = **1.00** | 156 s |
| Seoul | Cafes by ward | Spearman = **1.00** | ~90 s |

The Mumbai flood analysis reproduces a manually created QGIS benchmark with a Spearman correlation of **1.00**.

---

## Architecture

```
User
 │
 ▼
FastAPI
 │
Redis
 │
Celery
 │
├── Query Memory (Qdrant)
├── Data Retrieval (OSMnx / Overpass API)
├── Spatial Analysis
├── Result Validation
└── Result Storage
 │
 ▼
Interactive Leaflet Map
```

---

## Tech Stack

### Backend
- FastAPI
- Celery
- Redis
- PostgreSQL
- PostGIS
- Qdrant

### Geospatial
- GeoPandas
- Shapely
- OSMnx
- Overpass API
- rasterio
- WorldPop

### LLM
- Groq (Llama 3.3 70B)
- GPT-4o-mini
- BM25 + Dense Retrieval

### Frontend
- Leaflet.js

### Infrastructure
- Docker
- Azure
- Prometheus
- Grafana
- Langfuse

---

## Running Locally

```bash
git clone https://github.com/josaiahsyiem/nlgeo.git

cd nlgeo

cp .env.example .env

# Add your API keys

docker compose up -d --build
```

Open:

```
http://localhost:8000
```

Example query:

```
Which Mumbai wards have the highest flood-exposed population?
```

---

## Deployment

NLGeo runs as a containerized application on an Azure Virtual Machine using Docker Compose.

The deployment includes:

- FastAPI
- Celery workers
- PostgreSQL/PostGIS
- Redis
- Qdrant
- Grafana

The same Docker Compose configuration is used for both local development and deployment.

---

## About

NLGeo is a personal project built to make geospatial analysis more accessible through natural language. It combines traditional GIS techniques with modern language models to answer geographic questions and generate interactive maps without requiring GIS expertise.
