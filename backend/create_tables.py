from backend.database import Base, engine
from backend.models import Dataset

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")