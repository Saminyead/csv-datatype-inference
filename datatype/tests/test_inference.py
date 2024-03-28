import pytest
import pandas as pd
import numpy

from datatype.utils.inference import DataFrameToInfer
from datatype.utils.infer_all import infer_all

SAMPLE_DATA_PATH = "sample_data.csv"

@pytest.fixture
def df_test(filename:str=SAMPLE_DATA_PATH) -> pd.DataFrame:
    """Test Dataframe fixture"""
    return pd.read_csv(filename)


def test_infer_numeric_80_pct_col_is_numeric(df_test:DataFrameToInfer) -> None:
    """Test checks if infer_numeric categorizes columns with more than 80%
    numeric values as numeric"""
    df_to_infer_test: DataFrameToInfer = DataFrameToInfer(df_test)
    df_test_inferred: DataFrameToInfer = df_to_infer_test.infer_numeric()
    assert df_test_inferred['Score'].dtype == numpy.dtype('float')


def test_infer_datetime_varied_dt_formats(
        df_test:DataFrameToInfer
) -> None:
    """Test checks if infer_datetime categorizes columns containing a variety
    of datetime formats"""
    df_to_infer_test: DataFrameToInfer = DataFrameToInfer(df_test)
    df_test_inferred: DataFrameToInfer = df_to_infer_test.infer_datetime()
    assert df_test_inferred['Birthdate'].dtype == 'datetime64[ns]'
    assert df_test_inferred['Test_None_Datetime'].dtype == 'datetime64[ns]'


def test_infer_datetime_no_change_to_non_dt_formats(
        df_test:DataFrameToInfer
) -> None:
    """infer_datetime should not change other formats (especially integer 
    column that are still string/objects) to datetime formats"""
    df_to_infer_test: DataFrameToInfer = DataFrameToInfer(df_test)
    df_test_inferred: DataFrameToInfer = df_to_infer_test.infer_datetime()
    assert df_test_inferred['Test_None_Numeric'].dtype != 'datetime64[ns]'
    assert df_test_inferred['Test_All_Int'].dtype != 'datetime64[ns]'
    assert df_test_inferred['Score'].dtype != 'datetime64[ns]'


def test_infer_category_on_grades_col(
        df_test:pd.DataFrame
) -> None:
    """Test case to check if categorical data is inferred properly"""
    df_to_infer_test: DataFrameToInfer = DataFrameToInfer(df_test)
    df_test_inferred: DataFrameToInfer = df_to_infer_test.infer_category()
    assert df_test_inferred['Grade'].dtype == 'category'


def test_infer_bool(
        df_test:pd.DataFrame
) -> None:
    """Test case to check if boolean data is inferred properly"""
    df_to_infer_test = DataFrameToInfer(df_test)
    df_test_inferred = df_to_infer_test.infer_bool()
    assert df_test_inferred['Test_All_Bool'].dtype == 'bool'




def test_infer_all_inferred(
        csv_file:str = SAMPLE_DATA_PATH
) -> None:
    """Test to check if infer_all correctly infers the data types of all 
    column"""
    df_test_column_dtypes = infer_all(csv_file)

    assert df_test_column_dtypes['inferred_data_types']['Name'] == 'object'
    assert df_test_column_dtypes['inferred_data_types']['Grade'] == 'category'
    assert df_test_column_dtypes['inferred_data_types']['Remarks'] == 'category'
    assert df_test_column_dtypes['inferred_data_types']['Score'] == 'float64'
    assert df_test_column_dtypes['inferred_data_types']['Test_None_Numeric'] == 'float64'
    assert df_test_column_dtypes['inferred_data_types'][
        'Test_None_Datetime'] == 'datetime64[ns]'
    assert df_test_column_dtypes['inferred_data_types']['Birthdate'] == 'datetime64[ns]'
    assert df_test_column_dtypes['inferred_data_types']['Test_None_Datetime'] == 'datetime64[ns]'
    assert df_test_column_dtypes['inferred_data_types']['Test_All_Bool'] == 'bool'


# def test_infer_method_order_does_not_matter()