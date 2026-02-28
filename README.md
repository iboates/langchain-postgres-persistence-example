# LangGraph Postgres Checkpoint Demo

This example demonstrates:

- Pausing a LangGraph execution with `interrupt()`
- Persisting state in Postgres
- Resuming in a separate Python process
- Passing structured resume data (`approved`, optional `feedback`)

---

# Requirements

- Docker + Docker Compose
- Python 3.10+
- `uv` installed

---

# Project Structure

.
├── docker-compose.yml  
├── start.py  
├── resume.py  
├── pyproject.toml  

---

# 1. Start Postgres

From the project root:

```bash
docker compose up -d