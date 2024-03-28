import pandas as pd
from typing import Any
from datatype.utils.inference import DataFrameToInfer


def infer_all(csv_file:str) -> dict[str,Any]:
    df = pd.read_csv(csv_file)
    df_to_be_inferred = DataFrameToInfer(df)

    df_inferred = df_to_be_inferred.infer_numeric().\
        infer_datetime().infer_category().infer_bool()

    # applying formatting so that it prints dtype
    # original_data = df.to_js
    original_data_types = df.dtypes.apply(lambda x:x.name).to_dict()
    inferred_data_types = df_inferred.dtypes.apply(lambda x: x.name).to_dict()

    return {
        "original_data_json": df.to_json(orient='records',date_format='iso'),
        "original_data_types": original_data_types,
        "inferred_data_json": df_inferred.to_json(orient='records',date_format='iso'),
        "inferred_data_types": inferred_data_types
    }