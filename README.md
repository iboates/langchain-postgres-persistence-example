# LangGraph Postgres Checkpoint Demo

This example demonstrates:

- Pausing a LangGraph execution with `interrupt()`
- Persisting state in Postgres
- Resuming in a separate Python process
- Passing structured resume data (`approved`, optional `feedback`)

# Requirements

- Docker + Docker Compose
- Python 3.10+
- `uv` installed

# 1. Start Postgres

From the project root:

```bash
docker compose up -d
```

# 2. Install Dependencies (Fresh Setup)

If starting from scratch:

```
uv init --bare
uv add langgraph
uv add langgraph-checkpoint-postgres
uv add "psycopg[binary]"
uv sync
```

# 3. Start the Workflow

Run:

```
uv run python start.py
```

Output will include:

```
=== THREAD ID ===
<some-uuid>
=================

Paused with interrupt payload:
{...}
```

Copy the printed THREAD ID.

Execution is now paused and state is stored in Postgres.

# 4. Resume the Workflow

## Approve

```
uv run python resume.py <thread_id> true
```

## Reject With Feedback

```
uv run python resume.py <thread_id> false "Needs revision"
```
