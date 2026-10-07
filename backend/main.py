from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

from backend.s3_service import upload_file_to_s3
from backend.data_processor import clean_dataset, get_dataset_summary
from backend.anomaly_detector import detect_anomalies
from backend.database import SessionLocal
from backend.models import Dataset, Anomaly
from backend.s3_service import upload_file_to_s3, download_file_from_s3


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Intelligent Data Processing Platform API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # Read uploaded file
    file_content = await file.read()

    # Upload original file to S3
    s3_uri = upload_file_to_s3(
        file_content,
        file.filename
    )

    # Read CSV using the same file content
    df = pd.read_csv(
        io.BytesIO(file_content)
    )

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
        "s3_location": s3_uri,
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


@app.get("/anomalies")
def get_anomalies():

    db = SessionLocal()

    anomalies = db.query(Anomaly).all()

    db.close()

    return anomalies


@app.post("/process-s3")
def process_s3_file():

    file_content = download_file_from_s3("transactions.csv")

    df = pd.read_csv(
        io.BytesIO(file_content)
    )

    # Clean dataset
    df, processing_stats = clean_dataset(df)

    # Detect anomalies
    df, anomaly_stats = detect_anomalies(df)

    return {
        "filename": "transactions.csv",
        "processing": processing_stats,
        "summary": get_dataset_summary(df),
        "anomaly_detection": anomaly_stats
    }