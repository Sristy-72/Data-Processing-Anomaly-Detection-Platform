# Data-Processing-Anomaly-Detection-Platform

## About the Project

This project is a Python-based platform for processing datasets and finding unusual records in transaction data. It uses FastAPI to provide REST APIs for uploading and processing CSV files.

The platform cleans the uploaded data, removes invalid records, generates a summary, and uses the Isolation Forest algorithm to detect unusual transaction amounts. Uploaded files are stored in AWS S3, while dataset details and detected anomalies are stored in PostgreSQL.

## Features

- Upload CSV files through REST APIs.
- Clean data and remove invalid or missing records using Pandas.
- Generate dataset summaries, including total and average transaction amounts.
- Detect unusual transaction amounts using Isolation Forest.
- Store uploaded files in AWS S3.
- Store dataset information and detected anomalies in PostgreSQL.
- Process CSV files directly from S3.
- Run scheduled data processing.
- Test data processing functions and API endpoints using pytest.
- Run the FastAPI application inside Docker.

## Technologies Used

- **Language:** Python
- **Backend:** FastAPI, Uvicorn
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn, Isolation Forest
- **Database:** PostgreSQL, SQLAlchemy
- **Cloud Storage:** AWS S3, Boto3
- **Testing:** Pytest
- **Containerization:** Docker
- **Version Control:** Git and GitHub

## How It Works

1. A user uploads a CSV file through the API.
2. The original file is stored in AWS S3.
3. Pandas processes the data and removes invalid records.
4. Isolation Forest analyzes transaction amounts and identifies potential anomalies.
5. Dataset information and detected anomalies are stored in PostgreSQL.
6. The API returns the processing statistics, dataset summary, and anomaly results.

The platform also includes an endpoint for processing a CSV file that is already stored in S3.

## Project Structure

```text
Data-Processing-Anomaly-Detection-Platform/
│
├── backend/
│   ├── main.py
│   ├── data_processor.py
│   ├── anomaly_detector.py
│   ├── database.py
│   ├── models.py
│   ├── create_tables.py
│   ├── s3_service.py
│   └── scheduler.py
│
├── tests/
│   ├── test_anomaly_detector.py
│   ├── test_api.py
│   └── test_data_processor.py
│
├── data/
│   └── transactions.csv
│
├── requirements.txt
├── .gitignore
└── README.md
```

## API Endpoints

| Method | Endpoint      | Description                       |
| ------ | ------------- | --------------------------------- |
| GET    | `/`           | Returns the API welcome message   |
| GET    | `/health`     | Checks whether the API is running |
| POST   | `/upload`     | Uploads and processes a CSV file  |
| GET    | `/datasets`   | Returns saved dataset records     |
| GET    | `/anomalies`  | Returns saved anomaly records     |
| POST   | `/process-s3` | Processes a CSV file stored in S3 |

## Sample Results

The sample transaction dataset contains 18 records. After processing:

- Original records: 18
- Valid records: 15
- Removed records: 3
- Detected anomalies: 2
- Total transaction amount after cleaning: 104,770

The two detected anomalies are transactions T010 and T015, with amounts of 50,000 and 45,000 respectively.

These results are based on the sample dataset and the current Isolation Forest configuration.

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sristy-72/Data-Processing-Anomaly-Detection-Platform.git
cd Data-Processing-Anomaly-Detection-Platform
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it in Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your database and AWS configuration:

```env
DATABASE_URL=your_database_url
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your_bucket_name
```

Replace the example values with your own configuration. Never upload your `.env` file or AWS credentials to GitHub.

### 5. Create the database tables

Make sure PostgreSQL is running and the database exists. Then run:

```bash
python -m backend.create_tables
```

### 6. Start the application

```bash
uvicorn backend.main:app --reload
```

Open the interactive API documentation at:

`http://127.0.0.1:8000/docs`

## Running Tests

Run the test suite from the project root:

```bash
pytest
```

The tests cover data cleaning, anomaly detection, and the API health endpoint.

## Docker

A Dockerfile is available for running the FastAPI application in a container.

Build the image:

```bash
docker build -t data-processing-platform .
```

Run the container:

```bash
docker run --name data-processing-api -p 8000:8000 --env-file .env data-processing-platform
```

When running in Docker, make sure the database URL points to a PostgreSQL server accessible from the container.

## Future Improvements

- Improve API error handling and validation.
- Store S3 object references with dataset records.
- Add endpoints to retrieve anomalies for a specific dataset.
- Improve scheduled processing and monitoring.
- Add a dashboard to view processing results.
