# Kmeans API

This package provides API endpoints for creating, fitting, and retrieving K-means clustering data using FastAPI. The API supports asynchronous operations with background tasks, ensuring that large datasets can be processed without blocking the server.

---

## Table of Contents

- [Endpoints](#endpoints)
  - [Fit Kmeans](#fit-kmeans)
  - [Get Kmeans Centroids](#get-kmeans-centroids)
  - [Get Kmeans Data List](#get-kmeans-data-list)
  - [Delete Kmeans Data](#delete-kmeans-data)
- [Schemas](#schemas)
- [Models](#models)
- [CRUD Operations](#crud-operations)
- [Enums](#enums)
- [Background Task](#background-task)

---

## Endpoints

### Fit Kmeans

**POST** `/fit`

- Description: Fit a Kmeans model asynchronously and create a corresponding `KmeansData` record.
- Request body:
```json
  {
    "kmeans": {
      "n_clusters": 3,
      "max_iter": 100,
      "tol": 0.0001,
      "init": "kmeans++",
      "random_state": 1
    },
    "normalization": "z_score",
    "pca": {
      "n_components": 2,
      "random_state": 1
    },
    "description": "Optional description",
    "chat_id": "UUID of related chat"
  }
```

- Response:

```json
{
  "status": "Fit started"
}
```

### Get Kmeans Centroids

Get `Kmeans Centroids`

- Description: Retrieve the list
of centroids for a specific `KmeansData` by ID.
- Query parameters:
   - `skip` (default: 0)
   - `limit` (default: 10)
- Response:

```json
[
  {
    "id": "UUID",
    "values": [[...], [...], [...]],
    "fit_at": "datetime",
    "fit_time": 0.123,
    "kmeans_data": {
      "id": "UUID",
      "n_clusters": 3,
      "preprocessing": { "pca": "True", "normalization": "z_score" },
      "description": "string"
    }
  }
]
```

### Get Kmeans Data List
GET `/`

- Description: Retrieve a paginated list of `KmeansData`.
- Query parameters:
   - `skip` (default: 0)
   - `limit` (default: 10)
- Response: List of KmeansDataRead objects.

### Delete Kmeans Data

DELETE `/{kmeans_data_id}`

- Description: Delete a specific `KmeansData` and its related centroids.
- Response: HTTP 204 No Content

## Schemas

- `KmeansDataCreate` – Input schema for creating Kmeans data
- `KmeansDataRead` – Output schema for Kmeans data
- `KmeansDataDBCreate` – Internal DB schema for creation
- `KmeansCentroidCreate` – Input schema for centroids
- `KmeansCentroidRead` – Output schema for centroid
- `KmeansFit` – Input schema for the matrix X
- `KmeansScheme` – Kmeans configuration parameters
- `PCAInit` – PCA configuration parameters

## Models

- `KmeansData` – Represents Kmeans metadata, clusters count, preprocessing, and description.
- `KmeansCentroid` – Stores centroid values, fit time, and associated KmeansData.

## CRUD Operations

- `create_kmeans_data(db, scheme)` – Create KmeansData
- `create_kmeans_centroid(db, scheme)` – Create KmeansCentroid
- `read_kmeans_datas(db, skip, limit)` – Get list of KmeansData
- `read_kmeans_data(db, kmeans_data_id)` – Get KmeansData by ID
- `read_kmeans_centroids(db, kmeans_data_id, skip, limit)` – Get centroids
- `delete_kmeans_data(db, kmeans_data_id)` – Delete KmeansData

## Enums

- `KmeansInit` – Kmeans initialization method (kmeans++ or random)
- `Normalization` – Preprocessing normalization (z_score or minmax)

## Background Task

The `/fit` endpoint uses a background task to fit the Kmeans model asynchronously. This ensures that:

- The server does not block during heavy computation.
- The centroids are saved to the database after fitting.
- Preprocessing (normalization and PCA) is applied before fitting.

Example Usage

```python
from fastapi import FastAPI
from kmeans.router import kmeans_router


app = FastAPI()
app.include_router(kmeans_router, prefix="/kmeans")
```