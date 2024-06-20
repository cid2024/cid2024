# CID 2024

The Best Educational Social/History Test Questions Recommendation System

## Setup

### Requirements

- Python 3.11
- poetry

### 1. Install Python

**Mac OS**
```bash
brew install python@3.11
```

**Ubuntu**
```bash
sudo apt install python3.11
```

**Windows**
```bash
choco install python --version=3.11.0
```

### 2. Install poetry

https://python-poetry.org/docs/#installing-with-pipx

## Install dependencies

### Backend 

```bash
poetry install --no-root
```

### Frontend

```bash
cd frontend && npm install
```

## Run

### Backend

```bash
poetry run python -m backend.app
```

### Frontend

```bash
cd frontend && npm start build
```

Open http://localhost:3000/ in your browser.
