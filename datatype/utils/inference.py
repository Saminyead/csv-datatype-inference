import pandas as pd

from dateutil import parser

import numpy as np

# TODO: implement a class-based approach
class DataFrameToInfer(pd.DataFrame):
    """Class inheriting from DataFrame, so that infer methods can be
    directly applied to a DataFrame, and can be chained"""


    def infer_numeric(self) -> "DataFrameToInfer":
        """Finds which column of the dataframe are of a numeric type. 
        The criteria for the column to be numeric is - it has
        to have at least 80% of the entries as numeric.
        """
        # to prevent changing the original dataframe
        df: pd.DataFrame = self.copy()
        len_df: int = len(df)

        for col in df.columns:
            df_converted:pd.Series = pd.to_numeric(df[col], errors='coerce')
            len_df_converted_none: int = len(df_converted[df_converted.isna()])

            # checking whether the number of nan rows are less than 20% 
            # (thus >80% non-nan rows)
            if len_df_converted_none <= 0.2 * len_df:
                df[col] = df_converted

        return DataFrameToInfer(df)
    
    
    def _convert_to_datetime(self,col:pd.Series) -> pd.Series:
        """Helper function to convert column data type to datetime format"""
        col_dt:pd.Series = col.apply(
            lambda x: parser.parse(str(x), fuzzy=True).date() \
                if pd.notnull(x) else pd.NaT # type: ignore
        )
        col = col_dt
        col = pd.to_datetime(col)
        return col

    
    def infer_datetime(self) -> "DataFrameToInfer":
        """
        Goes through each column of dataframe to check if it contains datetime 
        values. If it does, then converts the column to datetime format 
        ('yyyy-mm-dd'), and coverts the column data type to datetime[ns64]
        """
        df = self.copy()
        for col in df.columns:
            if df[col].dtypes!='object':
                continue
            try:
                df[col] = self._convert_to_datetime(df[col])
            except (parser.ParserError, TypeError):
                continue
        return DataFrameToInfer(df)
    

    def infer_category(self) -> "DataFrameToInfer":
        """Finds which column of the dataframes are of type 'category'. 
        If the number of unique entries in the column is less than 50%, 
        the column is inferred as 'category'"""
        df = self.copy()
        for col in df.columns:
            if df[col].dtypes!='object':
                continue

            if df[col].nunique()/len(df[col]) < 0.5:
                df[col] = df[col].astype('category')

        return DataFrameToInfer(df)
    
    def infer_bool(self) -> "DataFrameToInfer":
        df = self.copy()
        for col in df.columns:
            try:
                # checked against Claude
                bool_vals = df[col].dropna().apply(
                    lambda x: isinstance(x,bool) or str(x).lower()\
                    in ['true','false','1','0']
                )

            except (ValueError,TypeError):
                continue

            if bool_vals.all():
                df[col] = df[col].replace(
                    ['True', 'true', 'TRUE', 1], True, inplace=False
                )
                df[col] = df[col].replace(
                    ['False', 'false', 'FALSE', 0], False, inplace=False
                )

                # to be checked against Claude
                df[col] = df[col].apply(
                    lambda x: True if x==True else False if x==False else np.nan
                )

        return DataFrameToInfer(df)



