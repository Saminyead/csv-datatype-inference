import pandas as pd

from datatype.utils.inference import (
    infer_datetime, infer_numeric
)


def infer_all(csv_file:str) -> dict[str,dict[str,str]]:
    df = pd.read_csv(csv_file)

    df_inferred = infer_numeric(df)
    df_inferred = infer_datetime(df_inferred)

    # applying formatting so that it prints dtype
    original_data_types = df.dtypes.apply(lambda x:x.name).to_dict()
    inferred_data_types = df_inferred.dtypes.apply(lambda x: x.name).to_dict()

    return {
        "original": original_data_types,
        "inferred": inferred_data_types
    }