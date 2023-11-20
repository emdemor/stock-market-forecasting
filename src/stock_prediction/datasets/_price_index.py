import zipfile

import pandas as pd
from datetime import datetime

from stock_prediction.config import config
from stock_prediction._utils import download_file


def get_ipca():
    return _format_price_index(config.IPCA_FILEPATH, index_name="ipca")


def get_inpc():
    return _format_price_index(config.INPC_FILEPATH, index_name="inpc")


def _format_price_index(filepath, index_name):
    string_to_avoid = [
        "SÉRIE HISTÓRICA DO IPCA",
        "SÉRIE HISTÓRICA DO INPC",
        "(continua)",
        "    VARIAÇÃO",
        "NÚMERO ÍNDICE",
        "(DEZ 93 = 100)",
        "MESES",
        "Fonte: IBGE, Diretoria de Pesquisas, Coordenação de Índices de Preços, ",
        "Sistema Nacional de Índices de Preços ao Consumidor.",
    ]

    months_mapping = {
        "JAN": 1,
        "FEV": 2,
        "MAR": 3,
        "ABR": 4,
        "MAI": 5,
        "JUN": 6,
        "JUL": 7,
        "AGO": 8,
        "SET": 9,
        "OUT": 10,
        "NOV": 11,
        "DEZ": 12,
    }
    columns = [
        "year",
        "month",
        "relative_to_dez93",
        "current_month",
        "last_3_months",
        "last_6_months",
        "current_year",
        "last_12_months",
    ]

    zip_local_filepath = filepath.split("/")[-1]
    download_file(filepath, zip_local_filepath)
    zf = zipfile.ZipFile(zip_local_filepath)
    last_file_name = sorted(zf.namelist())[-1]
    df = pd.read_excel(zf.open(last_file_name))
    df = df[df.notna().any(axis=1)]
    for string in string_to_avoid:
        df = df[~(df == string).any(axis=1)]
    for col, n_not_null in df.notna().sum().to_dict().items():
        if n_not_null == 0:
            df = df.drop(columns=[col])
    df.columns = columns
    df = df[df["month"].isin(months_mapping)]
    df["year"] = df["year"].fillna(method="ffill")
    df["month"] = df["month"].replace(months_mapping)
    df[df.columns[2:]] = df[df.columns[2:]] / 100
    replaces = {col: index_name + "_" + col for col in df.columns[2:]}
    df = df.rename(columns=replaces)
    df["date"] = df.apply(
        lambda row: datetime(row["year"], row["month"], 1) + pd.offsets.MonthEnd(0),
        axis=1,
    )
    df = df[["date"] + list(replaces.values())]

    data = data.set_index("date")
    
    return df
