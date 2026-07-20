@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/projects")
def list_projects() -> list[dict]:
    # Mock projects endpoint
    return [{"id": 1, "name": "ASEP Platform", "status": "running"}]


@app.get("/api/v1/projects")
def list_projects() -> list[dict]:
    # Mock projects endpoint
    return [{"id": 1, "name": "ASEP Platform", "status": "running"}]


@app.get("/api/v1/projects")
def list_projects() -> list[dict]:
    # Mock projects endpoint
    return [{"id": 1, "name": "ASEP Platform", "status": "running"}]


@app.get("/api/v1/projects")
def list_projects() -> list[dict]:
    # Mock projects endpoint
    return [{"id": 1, "name": "ASEP Platform", "status": "running"}]
