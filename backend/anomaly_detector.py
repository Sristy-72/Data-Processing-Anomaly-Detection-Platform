import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df):
    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    predictions = model.fit_predict(df[["amount"]])

    df["is_anomaly"] = predictions == -1

    anomaly_count = int(df["is_anomaly"].sum())
    total_records = len(df)

    anomaly_rate = (
        anomaly_count / total_records * 100
        if total_records > 0
        else 0
    )
    
    anomalies = df[df["is_anomaly"]].to_dict(orient="records")


    stats = {
        "total_records": total_records,
        "anomaly_count": anomaly_count,
        "anomaly_rate": round(anomaly_rate, 2),
        "anomalies": anomalies
    }

    return df, stats

if __name__ == "__main__":
    df = pd.read_csv("data/transactions.csv")

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df = df.dropna(subset=["amount"])

    df, anomaly_stats = detect_anomalies(df)
   

    print(df[["transaction_id", "amount", "is_anomaly"]])

    print("\nAnomaly Statistics:")
    print(anomaly_stats)