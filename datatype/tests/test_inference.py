import pytest
import pandas as pd
import numpy

from datatype.utils.inference import (
    infer_numeric, infer_datetime
)

SAMPLE_DATA_PATH = "sample_data.csv"

# TODO: create a fixture - a dataframe from a CSV file
@pytest.fixture
def df_test(filename:str=SAMPLE_DATA_PATH) -> pd.DataFrame:
    """Test Dataframe fixture"""
    return pd.read_csv(filename)


def test_infer_numeric_80_pct_col_is_numeric(df_test:pd.DataFrame) -> None:
    """Test checks if infer_numeric categorizes columns with more than 80%
    numeric values as numeric"""
    df_test_inferred: pd.DataFrame = infer_numeric(df_test)
    assert df_test_inferred['Score'].dtype == numpy.dtype('float')



def test_infer_datetime_varied_dt_formats(
        df_test:pd.DataFrame
) -> None:
    """Test checks if infer_datetime categorizes columns containing a variety
    of datetime formats"""
    df_test_inferred: pd.DataFrame = infer_datetime(df_test)
    assert df_test_inferred['Birthdate'].dtype == 'datetime64[ns]'
    assert df_test_inferred['Test_None_Datetime'].dtype == 'datetime64[ns]'


def test_infer_datetime_no_change_to_non_dt_formats(
        df_test:pd.DataFrame
) -> None:
    """infer_datetime should not change other formats (especially integer 
    column that are still string/objects) to datetime formats"""
    df_test_inferred: pd.DataFrame = infer_datetime(df_test)
    assert df_test_inferred['Test_None_Numeric'].dtype != 'datetime64[ns]'
    assert df_test_inferred['Test_All_Int'].dtype != 'datetime64[ns]'
    assert df_test_inferred['Score'].dtype != 'datetime64[ns]'
