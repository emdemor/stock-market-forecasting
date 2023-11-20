# https://railandeivid.medium.com/usando-a-biblioteca-sidrapy-para-acessar-a-api-sidra-do-ibge-usando-python-1ef81a036f50
# https://apisidra.ibge.gov.br/home

import sidrapy

from stock_prediction.datasets._tools import (
    format_sidra_result,
    set_date_from_monthcode,
)


IPP_COLUMNS_MAPPING = {
    "Valor": "value",
    "Indústria geral, indústrias extrativas e indústrias de transformação e atividades (CNAE 2.0)": "industry_sector",
    "Mês (Código)": "month_code",
    "Variável": "variable",
}

IPP_VALUES_MAPPING = {
    "variable": {
        "IPP - Número-índice (dezembro de 2018 = 100)": "ipp_n_indice",
        "IPP - Variação acumulada no ano (em relação a dezembro do ano anterior)": "ipp_current_year",
        "IPP - Variação mês/mesmo mês do ano anterior (M/M-12)": "ipp_last_year",
        "IPP - Variação mês/mês imediatamente anterior (M/M-1)": "ipp_last_month",
    },
    "industry_sector": {
        "Indústria Geral": "general",
        "B Indústrias Extrativas": "extractive",
        "C Indústrias de Transformação": "transformation",
        "10 FABRICAÇÃO DE PRODUTOS ALIMENTÍCIOS": "food",
        "11 FABRICAÇÃO DE BEBIDAS": "drink",
        "12 FABRICAÇÃO DE PRODUTOS DO FUMO": "smoking",
        "13 FABRICAÇÃO DE PRODUTOS TÊXTEIS": "textile",
        "14 CONFECÇÃO DE ARTIGOS DO VESTUÁRIO E ACESSÓRIOS": "clothes",
        "15 PREPARAÇÃO DE COUROS E FABRICAÇÃO DE ARTEFATOS DE COURO, ARTIGOS PARA VIAGEM E CALÇADOS": "leather_or_shoes",
        "16 FABRICAÇÃO DE PRODUTOS DE MADEIRA": "wood",
        "17 FABRICAÇÃO DE CELULOSE, PAPEL E PRODUTOS DE PAPEL": "paper",
        "18 IMPRESSÃO E REPRODUÇÃO DE GRAVAÇÕES": "printing",
        "19 FABRICAÇÃO DE COQUE, DE PRODUTOS DERIVADOS DO PETRÓLEO E DE BIOCOMBUSTÍVEIS": "petrochemicals_fuels_biofuels",
        "20B FABRICAÇÃO DE SABÕES, DETERGENTES, PRODUTOS DE LIMPEZA, COSMÉTICOS, PRODUTOS DE PERFUMARIA E DE HIGIENE PESSOAL": "hygiene_and_cleaning",
        "20C FABRICAÇÃO DE OUTROS PRODUTOS QUÍMICOS": "chemicals",
        "21 FABRICAÇÃO DE PRODUTOS FARMOQUÍMICOS E FARMACÊUTICOS": "pharmaceutical",
        "22 FABRICAÇÃO DE PRODUTOS DE BORRACHA E DE MATERIAL PLÁSTICO": "rubber_and_plastic",
        "23 FABRICAÇÃO DE PRODUTOS DE MINERAIS NÃO METÁLICOS": "non_metallic_minerals",
        "24 METALURGIA": "metallurgy",
        "25 FABRICAÇÃO DE PRODUTOS DE METAL, EXCETO MÁQUINAS E EQUIPAMENTOS": "metal_products_except_machines_and_equipment",
        "26 FABRICAÇÃO DE EQUIPAMENTOS DE INFORMÁTICA, PRODUTOS ELETRÔNICOS E ÓPTICOS": "it_electronics_and_optics",
        "27 FABRICAÇÃO DE MÁQUINAS, APARELHOS E MATERIAIS ELÉTRICOS": "eletrical_machine_apparatus_and_materials",
        "28 FABRICAÇÃO DE MÁQUINAS E EQUIPAMENTOS": "machines_and_equipment",
        "29 FABRICAÇÃO DE VEÍCULOS AUTOMOTORES, REBOQUES E CARROCERIAS": "motor_vehicles",
        "30 FABRICAÇÃO DE OUTROS EQUIPAMENTOS DE TRANSPORTE, EXCETO VEÍCULOS AUTOMOTORES": "transportation_equipment_except_vehicles",
        "31 FABRICAÇÃO DE MÓVEIS": "fornitures",
    },
}


def get_ipp():
    data_raw = sidrapy.get_table(
        table_code="6903",
        territorial_level="1",
        ibge_territorial_code="all",
        period="all",
        classifications={842: "all"},
    )

    df = format_sidra_result(
        data_raw,
        columns_mapping=IPP_COLUMNS_MAPPING,
        values_mapping=IPP_VALUES_MAPPING,
        pivot_columns=["variable", "industry_sector"],
    )
    df.columns = [str(_[0]) + "_" + str(_[1]) for i, _ in enumerate(df.columns)]
    df = df / 100

    df = set_date_from_monthcode(df)

    df = df.set_index("date")

    return df
