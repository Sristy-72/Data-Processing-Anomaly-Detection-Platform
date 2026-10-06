from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Intelligent Data Processing Platform API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}