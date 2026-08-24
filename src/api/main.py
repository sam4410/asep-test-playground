
# Static files
if os.path.exists("static") and os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Other routes and configurations...