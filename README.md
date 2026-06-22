# ASEP

Autonomous Software Engineering Platform.

Phase 1 focuses on basic planning and coding with PostgreSQL-backed shared memory,
task queue state, and event logging.

## Local Setup

```powershell
conda activate asep
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
docker compose up -d postgres
asep db migrate
```

## First Commands

```powershell
asep plan "Build a simple feature"
asep status
asep tasks list
asep memory list
```
