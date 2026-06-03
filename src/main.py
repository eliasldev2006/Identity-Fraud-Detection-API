from fastapi import FastAPI

app = FastAPI(
    title="Identity Fraud Detection API"
)

@app.get("/")
def home():
    return {"status": "online"}