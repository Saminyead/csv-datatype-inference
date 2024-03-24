import pandas as pd

from dateutil import parser


# TODO: implement a class-based approach

def infer_numeric(df:pd.DataFrame) -> pd.DataFrame:
    """Finds which column of the dataframe are of a numeric type. 
    The criteria for the column to be numeric is - it has
    to have at least 80% of the entries as numeric.

    Args:
        df (pd.DataFrame): dataframe whose column's data type is to be inferred

    Returns:
        pd.DataFrame: the dataframe with the correct data column data type
    """
    df = df.copy()      # to prevent changing the original dataframe
    len_df: int = len(df)

    for col in df.columns:
        df_converted:pd.Series = pd.to_numeric(df[col], errors='coerce')
        len_df_converted_none: int = len(df_converted[df_converted.isna()])

        if len_df_converted_none <= 0.2 * len_df:
            df[col] = df_converted

    return df



def _convert_to_datetime(col:pd.Series) -> pd.Series:
    """Helper function to convert column data type to datetime format"""
    col_dt:pd.Series = col.apply(
        lambda x: parser.parse(str(x), fuzzy=True).date() \
            if pd.notnull(x) else pd.NaT # type: ignore
    )
    col = col_dt
    col = pd.to_datetime(col)
    return col

def infer_datetime(df:pd.DataFrame) -> pd.DataFrame:
    """
    Goes through each column of dataframe to check if it contains datetime 
    values. If it does, then converts the column to datetime format 
    ('yyyy-mm-dd'), and coverts the column data type to datetime[ns64]
    
    Args:
        df (pandas.DataFrame): The dataframe whose columns are to be 
            converted.
        
    Returns:
        pandas.DataFrame: The converted column with datetime format 
            ('yyyy-mm-dd').
    """
    df = df.copy()
    for col in df.columns:
        if df[col].dtypes!='object':
            continue
        try:
            df[col] = _convert_to_datetime(df[col])
        except (parser.ParserError, TypeError):
            continue
    return df