from fastapi import FastAPI

app = FastAPI(title="PakimonGO API", version="0.1.0")

@app.get("/health/live")
def health_live():
    return {"status": "ok"}

@app.get("/health/ready")
def health_ready():
    return {"status": "ok"}
