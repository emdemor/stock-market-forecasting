import sidrapy

from stock_prediction.datasets._tools import (
    format_sidra_result,
    normalize_column_name,
    set_date_from_quartercode,
)


PIB_COLUMNS_MAPPING = {
    "Variável": "variable",
    "Trimestre (Código)": "quarter_code",
    "Valor": "value",
}

PIB_VALUES_MAPPING = {}

PIB_SECTORS_COLUMNS_MAPPING = {
    "Variável": "variable",
    "Trimestre (Código)": "quarter_code",
    "Valor": "value",
    "Setores e subsetores": "sector",
}

PIB_SECTORS_VALUES_MAPPING = {
    "variable": {
        "Valores a preços correntes": "pib_setores",
    }
}


def get_pib():
    pib_raw = sidrapy.get_table(
        table_code="2072",
        territorial_level="1",
        ibge_territorial_code="all",
        period="all",
    )

    pib_setores_raw = sidrapy.get_table(
        table_code="1846",
        territorial_level="1",
        ibge_territorial_code="all",
        period="all",
        classifications={11255: "all"},
    )

    pib = format_sidra_result(
        pib_raw,
        columns_mapping=PIB_COLUMNS_MAPPING,
        values_mapping=PIB_VALUES_MAPPING,
        pivot_columns=["variable"],
        freq="quarter",
    )
    pib_setores = format_sidra_result(
        pib_setores_raw,
        columns_mapping=PIB_SECTORS_COLUMNS_MAPPING,
        values_mapping=PIB_SECTORS_VALUES_MAPPING,
        pivot_columns=["variable", "sector"],
        freq="quarter",
    )

    pib_setores.columns = [normalize_column_name(x[1]) for x in pib_setores.columns]

    pib_setores = set_date_from_quartercode(pib_setores)

    pib.columns = [normalize_column_name(x) for x in pib.columns]

    pib = set_date_from_quartercode(pib)

    data = data.set_index("date")

    return pib_setores.merge(pib, how="outer", on="date")
