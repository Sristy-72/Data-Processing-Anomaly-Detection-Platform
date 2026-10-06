from fastapi import FastAPI, UploadFile, File
import pandas as pd

from backend.data_processor import clean_dataset, get_dataset_summary

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Intelligent Data Processing Platform API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    original_records = len(df)

    df, processing_stats = clean_dataset(df)

    summary = get_dataset_summary(df)

    return {
        "filename": file.filename,
        "processing": processing_stats,
        "summary": summary
    }