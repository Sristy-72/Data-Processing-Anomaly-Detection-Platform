import pandas as pd


def load_dataset(file_path):
    df = pd.read_csv(file_path)

    return df


def clean_dataset(df):
    original_count = len(df)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert amount to numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Remove rows with invalid/missing values
    df = df.dropna()

    cleaned_count = len(df)

    stats = {
        "original_records": original_count,
        "cleaned_records": cleaned_count,
        "removed_records": original_count - cleaned_count
    }

    return df, stats

def get_dataset_summary(df):
    return {
        "total_records": len(df),
        "columns": list(df.columns),
        "average_amount": df["amount"].mean(),
        "total_amount": df["amount"].sum(),
    }


if __name__ == "__main__":
    df = load_dataset("data/transactions.csv")

    df, processing_stats = clean_dataset(df)

    summary = get_dataset_summary(df)

    print(summary)
    print(processing_stats)  