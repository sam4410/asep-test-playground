
# Static files
# Ensure the 'static' directory exists or comment out the following line
if os.path.exists("static") and os.path.isdir("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.on_event("startup")