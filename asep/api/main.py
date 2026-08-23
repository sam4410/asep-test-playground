
# Mount static files if the directory exists
import os
if os.path.exists("static") and os.path.isdir("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.on_event("startup")