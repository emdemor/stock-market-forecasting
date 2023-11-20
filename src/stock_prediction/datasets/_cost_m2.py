from datetime import datetime

import sidrapy
import numpy as np


from stock_prediction.datasets._tools import (
    format_sidra_result,
    set_date_from_monthcode,
)


M2_COST_COLUMNS_MAPPING = {
    "Variável": "variable",
    "Mês (Código)": "month_code",
    "Valor": "value",
}

M2_COST_VALUES_MAPPING = {
    "variable": {
        "Custo médio m² - moeda corrente": "cost_m2",
        "Custo médio m² - número-índice": "cost_m2_index",
        "Custo médio m² - componente material - moeda corrente": "cost_m2_material",
        "Custo médio m² - componente mão-de-obra - moeda corrente": "cost_m2_labor",
        "Custo médio m² - componente material - número-índice": "cost_m2_material_index",
        "Custo médio m² - componente mão-de-obra - número-índice": "cost_m2_labor_index",
        "Custo médio m² - variação percentual no mês": "cost_m2_month_variation",
        "Custo médio m² - variação percentual no ano": "cost_m2_current_year_variation",
        "Custo médio m² - variação percentual em doze meses": "cost_m2_last_year_variation",
    }
}


def get_m2_cost():
    data_raw = sidrapy.get_table(
        table_code="2296",
        territorial_level="1",
        ibge_territorial_code="all",
        period="all",
    )
    data = format_sidra_result(
        data_raw,
        columns_mapping=M2_COST_COLUMNS_MAPPING,
        values_mapping=M2_COST_VALUES_MAPPING,
        pivot_columns=["variable"],
    )

    index_columns = [x for x in data.columns if "index" in x]

    data[index_columns] = data[index_columns] / 100

    data = set_date_from_monthcode(data)

    for col in index_columns:
        data[col] = np.where(data["date"] < datetime(2012, 9, 1), np.nan, data[col])
    
    data.columns = list(data.columns)

    return data
