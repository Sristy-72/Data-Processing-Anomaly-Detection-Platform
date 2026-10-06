from fastapi import FastAPI, UploadFile, File
import pandas as pd

from backend.data_processor import clean_dataset, get_dataset_summary
from backend.anomaly_detector import detect_anomalies
from backend.database import SessionLocal
from backend.models import Dataset, Anomaly


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

    # Clean dataset
    df, processing_stats = clean_dataset(df)

    # Detect anomalies
    df, anomaly_stats = detect_anomalies(df)

    # Database session
    db = SessionLocal()

    # Save dataset
    dataset = Dataset(
        filename=file.filename,
        total_records=len(df)
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    # Save anomalies
    for _, row in df[df["is_anomaly"]].iterrows():
        anomaly = Anomaly(
            dataset_id=dataset.id,
            transaction_id=row["transaction_id"],
            amount=row["amount"],
            category=row["category"],
            user_id=row["user_id"]
        )

        db.add(anomaly)

    db.commit()
    db.close()

    # Generate summary
    summary = get_dataset_summary(df)

    return {
        "filename": file.filename,
        "processing": processing_stats,
        "summary": summary,
        "anomaly_detection": anomaly_stats
    }


@app.get("/datasets")
def get_datasets():
    db = SessionLocal()

    datasets = db.query(Dataset).all()

    db.close()

    return datasets