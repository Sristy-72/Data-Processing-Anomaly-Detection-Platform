import pandas as pd

from backend.data_processor import clean_dataset


def test_clean_dataset_removes_invalid_rows():

    df = pd.DataFrame({
        "transaction_id": ["T001", "T002", "T003"],
        "date": ["2026-01-01", "invalid-date", "2026-01-03"],
        "amount": [500, 700, "abc"],
        "category": ["Food", "Shopping", "Food"],
        "user_id": ["U001", "U002", "U003"]
    })

    cleaned_df, stats = clean_dataset(df)

    assert len(cleaned_df) == 1
    assert stats["original_records"] == 3
    assert stats["cleaned_records"] == 1
    assert stats["removed_records"] == 2