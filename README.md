# NLGeo

**Ask geographic questions in plain English and get interactive maps in seconds.**

🎥 **[Demo Video](https://youtu.be/h7c9p2f2qqk)**

---

## Overview

NLGeo is a geospatial analysis application that lets users query OpenStreetMap data using natural language instead of GIS software or SQL.

Ask questions like **"Which Mumbai wards have the highest flood-exposed population?"** or **"How many pharmacies are there in each Berlin district?"**, and NLGeo retrieves the required data, performs the analysis, validates the results, and generates an interactive choropleth map.

The project combines traditional GIS workflows with large language models, using deterministic spatial analysis whenever possible and falling back to LLM-generated geospatial code for more complex queries.

---

## Features

- Ask geographic questions in plain English
- Interactive choropleth maps
- Live OpenStreetMap data retrieval
- Deterministic spatial analysis with LLM fallback
- Automatic result validation
- Multi-city support
- Population-normalized analysis using WorldPop
- Spatial joins using uploaded datasets
- CSV and GeoJSON export

---

## Workflow

1. Search vector memory for similar queries.
2. Convert the request into a structured analysis plan.
3. Retrieve administrative boundaries and OpenStreetMap features.
4. Run deterministic GIS analysis whenever possible.
5. Generate geospatial code with an LLM for unsupported queries.
6. Validate the output.
7. Return an interactive map with the computed metrics.

---

## Results

NLGeo has been tested across more than **20 cities** covering flood analysis, healthcare accessibility, greenspace analysis, population-normalized metrics, and spatial joins.

| City | Example Query | Validation |
|------|---------------|-----------:|
| Mumbai | Flood exposure by ward | Spearman = **1.00** |
| Berlin | Pharmacies by district | Spearman = **1.00** |
| Greater London | Hospitals by ward | Spearman = **1.00** |
| Paris | Restaurants by arrondissement | Spearman = **1.00** |
| Seoul | Cafes by ward | Spearman = **1.00** |
| New Delhi | Hospitals by area | Spearman = **1.00** |
| Cairo | Schools by area | Spearman = **1.00** |
| Lagos | Greenspace analysis | ✓ |
| Bengaluru | Hospital coverage (file upload) | ✓ |
| Kolkata | Hospital density (file upload) | ✓ |

The Mumbai flood analysis reproduces a manually created QGIS benchmark with a Spearman correlation of **1.00**.

Repeated queries are served from vector memory, avoiding unnecessary recomputation and improving response time.

---

## Architecture

```text
                +------------------+
                |      User        |
                +--------+---------+
                         |
                         v
                  +-------------+
                  |   FastAPI   |
                  +------+------+ 
                         |
                         v
                    +---------+
                    |  Redis  |
                    +----+----+
                         |
                         v
                    +---------+
                    | Celery  |
                    +----+----+
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
+---------------+ +---------------+ +----------------+
| Query Memory  | | Data Retrieval| | Spatial Analysis|
|   (Qdrant)    | | OSMnx/Overpass| |                |
+---------------+ +---------------+ +----------------+
                         |
                         v
                 +---------------+
                 |  Validation   |
                 +-------+-------+
                         |
                         v
                 +---------------+
                 | Leaflet Map   |
                 +---------------+
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

Clone the repository.

```bash
git clone https://github.com/josaiahsyiem/nlgeo.git
cd nlgeo
```

Create your environment file.

```bash
cp .env.example .env
```

Add your API keys to `.env`.

Start the application.

```bash
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

NLGeo runs on an Azure Virtual Machine using Docker Compose.

The deployment includes:

- FastAPI
- Celery
- PostgreSQL/PostGIS
- Redis
- Qdrant
- Grafana

The same Docker Compose configuration is used for both local development and deployment.
