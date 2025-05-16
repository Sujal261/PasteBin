# 📝 Pastebin Clone

A lightweight, fast, and secure Pastebin clone built with **FastAPI** and **SQLite**. Create and share text snippets with optional password protection and expiration.

---

## 🚀 Features

- Create public or private pastes
- Optional password protection
- Set expiration time
- View and manage pastes via API
- SQLite-backed storage
- Docker & local deployment supported

---

## 📦 Tech Stack

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

---

## 📑 Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [API Documentation](#api-documentation)
4. [Database Schema](#database-schema)
5. [Deployment](#deployment)
6. [Development](#development)
7. [Troubleshooting](#troubleshooting)
8. [License](#license)

---

## 🔧 Installation

### 📍 Local

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🐳 Docker

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

### 🔨 Build and Run the Container

```bash
docker build -t pastebin-clone .
docker run -p 8000:8000 pastebin-clone
```


## 📖 API Documentation

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

### 🧭 Endpoints

| Endpoint         | Method | Parameters                             | Description              |
|------------------|--------|----------------------------------------|--------------------------|
| `/create`        | POST   | `content`, `user_id`, `password?`, `expires_after?` | Create new paste         |
| `/view/{url_id}` | GET    | `password?`                            | View paste content       |
| `/info/{url_id}` | GET    | –                                      | Get paste metadata       |
| `/test-db`       | GET    | –                                      | Test database connection |

### 🧪 Example Requests

#### 🔸 Create a Paste

```bash
curl -X POST "http://localhost:8000/create" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "content=HelloWorld&user_id=user123"
```

#### Create a Protected Pase with expiration

```bash
curl -X POST "http://localhost:8000/create" \
     -d "content=Secret&user_id=user123&password=mypass&expires_after=60"
```

```bash

#### View a Paste

```bash
curl "http://localhost:8000/view/abc123def"
```


#### View a Protected Paste

```bash
curl "http://localhost:8000/view/ghi456jkl?password=mypass"
```

## 🗄️ Database Schema

**SQLite File:** `database/content.db`

```sql
CREATE TABLE pastes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    user_id TEXT NOT NULL,
    url_id TEXT UNIQUE NOT NULL,
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_private BOOLEAN DEFAULT FALSE
);
```


## 🛠️ Development

### 📁 Project Structure

```text
pastebin-clone/
├── app/
│   ├── main.py            # FastAPI application and routes
│   └── database.py        # Database operations
├── database/              # SQLite database
│   └── content.db
├── tests/                 # Unit tests
├── requirements.txt       
└── README.md
```

## Running Tests

```bash 
pytest tests/test_main.py
```









