import pandas as pd

from backend.anomaly_detector import detect_anomalies


def test_anomaly_detection():

    df = pd.DataFrame({
        "transaction_id": [
            "T001", "T002", "T003", "T004",
            "T005", "T006", "T007", "T008",
            "T009", "T010"
        ],
        "amount": [
            500, 600, 550, 700, 650,
            800, 750, 900, 850, 50000
        ]
    })

    result_df, stats = detect_anomalies(df)

    assert "is_anomaly" in result_df.columns
    assert stats["total_records"] == 10
    assert stats["anomaly_count"] >= 1