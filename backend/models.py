from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from datetime import datetime

from backend.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    total_records = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)

    transaction_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    user_id = Column(String, nullable=True)