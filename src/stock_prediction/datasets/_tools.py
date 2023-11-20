from datetime import datetime

import numpy as np
import pandas as pd
from unidecode import unidecode


def set_date_from_monthcode(df):
    if df.index.name == "month_code":
        df = df.reset_index()
    if "month_code" not in df.columns:
        raise ValueError("'month_code' not found in columns.")

    df["year"] = df["month_code"].str[:4].astype(int)
    df["month"] = df["month_code"].str[4:6].astype(int)
    df["date"] = df.apply(
        lambda row: datetime(row["year"], row["month"], 1) + pd.offsets.MonthEnd(0),
        axis=1,
    )
    df = df.drop(columns=["year", "month", "month_code"])
    df = df[["date"] + [x for x in df.columns if x != "date"]]
    return df


def set_date_from_quartercode(df):
    quarter_mapping = [3, 6, 9, 12]

    if df.index.name == "quarter_code":
        df = df.reset_index()
    if "quarter_code" not in df.columns:
        raise ValueError("'quarter_code' not found in columns.")

    df["year"] = df["quarter_code"].str[:4].astype(int)
    df["month"] = (
        df["quarter_code"].str[4:6].astype(int).apply(lambda x: quarter_mapping[x - 1])
    )

    df["date"] = df.apply(
        lambda row: datetime(row["year"], row["month"], 1) + pd.offsets.MonthEnd(0),
        axis=1,
    )
    df = df.drop(columns=["year", "month", "quarter_code"], errors="ignore")
    df = df[["date"] + [x for x in df.columns if x != "date"]]
    return df


def format_sidra_result(
    data_raw,
    columns_mapping=None,
    values_mapping=None,
    pivot_columns=None,
    freq="monthly",
):
    periods = {
        "monthly": "month_code",
        "daily": "day_code",
        "quarter": "quarter_code",
        "yearly": "year_code",
    }

    value_column = "Valor"
    period_column = periods[freq]

    data = data_raw.iloc[1:]
    data.columns = data_raw.iloc[0]

    data[value_column] = data[value_column].apply(lambda x: _to_number(x))

    if columns_mapping:
        data = data[columns_mapping.keys()]
        data.columns = columns_mapping.values()

        if value_column in columns_mapping:
            value_column = columns_mapping[value_column]

        if period_column in columns_mapping:
            period_column = columns_mapping[period_column]

    if values_mapping:
        for col in values_mapping:
            data[col] = data[col].replace(values_mapping[col])

    if pivot_columns:
        data = data.pivot_table(
            values=value_column, index=period_column, columns=pivot_columns
        )

    return data


def _to_number(x):
    try:
        return float(x)
    except ValueError:
        return np.nan


def normalize_column_name(column_name):
    column_name = unidecode(column_name.lower())
    column_name = column_name.replace(" ", "_")
    column_name = "".join(c if c.isalnum() or c == "_" else "" for c in column_name)
    column_name = column_name.replace("__", "_")
    while (not column_name[0].isalpha()) and len(column_name) > 1:
        column_name = column_name[1:]
    return column_name
