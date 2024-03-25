import pandas as pd

from datatype.utils.inference import DataFrameToInfer


def infer_all(csv_file:str) -> dict[str,dict[str,str]]:
    df = pd.read_csv(csv_file)
    df_to_be_inferred = DataFrameToInfer(df)

    df_inferred = df_to_be_inferred.infer_numeric().infer_datetime()

    # applying formatting so that it prints dtype
    original_data_types = df.dtypes.apply(lambda x:x.name).to_dict()
    inferred_data_types = df_inferred.dtypes.apply(lambda x: x.name).to_dict()

    return {
        "original": original_data_types,
        "inferred": inferred_data_types
    }