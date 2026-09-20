from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ask")
def ask_llm():
    return {"status": "ok"}