import pandas as pd
from typing import Any
from datatype.utils.inference import DataFrameToInfer

DATA_TYPE_TO_READABLE_DATA_TYPE_MAP: dict[str,str] = {
    "object":"Text",
    "datetime64[ns]":"Date and Time",
    "category":"Categorical Data",
    "float64":"Numeric (Floating Points)",
    "int64":"Numeric (Integer)",
    "bool":"Boolean"
}

def infer_all(csv_file:str) -> dict[str,Any]:
    df = pd.read_csv(csv_file)
    df_to_be_inferred = DataFrameToInfer(df)

    df_inferred = df_to_be_inferred.infer_numeric().\
        infer_datetime().infer_category().infer_bool()

    # applying formatting so that it prints dtype
    # original_data = df.to_js
    original_data_types = df.dtypes.apply(lambda x:x.name).to_dict()
    inferred_data_types = df_inferred.dtypes.apply(lambda x: x.name).to_dict()

    original_data_types_readable:dict[str,str] = {
        key:DATA_TYPE_TO_READABLE_DATA_TYPE_MAP[value] for\
              key,value in original_data_types.items()
    }

    inferred_data_types_readable:dict[str,str] = {
        key:DATA_TYPE_TO_READABLE_DATA_TYPE_MAP[value] for\
              key,value in inferred_data_types.items()
    }

    return {
        "original_data_json": df.to_json(orient='records',date_format='iso'),
        "original_data_types": original_data_types,
        "original_data_types_readable":original_data_types_readable,
        "inferred_data_json": df_inferred.to_json(orient='records',date_format='iso'),
        "inferred_data_types": inferred_data_types,
        "inferred_data_types_readable": inferred_data_types_readable,
    }