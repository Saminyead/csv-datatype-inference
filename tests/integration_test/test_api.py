import pytest
from rest_framework.test import APIClient
from rest_framework.response import Response
import pandas as pd
import pathlib


INVALID_FILE: pathlib.Path = pathlib.Path(__file__).resolve().parent\
    /'files'/'invalid.pdf'
DATA_FILE:pathlib.Path = pathlib.Path(__file__).resolve().parent\
    /'files'/'data.csv'


@pytest.mark.django_db
def test_api_invalid_file_format(
    api_client:APIClient,
    api_endpoint: str,
    filename:str = INVALID_FILE
) -> None:
    response:Response = api_client.post(
        path=api_endpoint,
        data={'file':f'{filename}'},
        format='multipart'
    )

    assert response.status_code == 400



@pytest.mark.django_db
def test_api_data_inferred_types(
    api_client:APIClient,
    api_endpoint: str,
    filename:str = DATA_FILE
) -> None:
    response:Response = api_client.post(
        path=api_endpoint,
        data={'file':open(filename)},
        format='multipart'
    )

    expected_values:dict= {
        'Birthdate':'datetime64[ns]',
        'Test_None_Datetime':'datetime64[ns]',
        'Score':'float64',
        'Test_None_Numeric':'float64',
        'Test_All_Int':'int64',
    }

    assert response.status_code == 201
    
    for value in expected_values:
        assert value in response.data['inferred_data']['inferred_data_types']


@pytest.mark.django_db
def test_response_dataframes(
    api_client:APIClient,
    api_endpoint:str,
    filename:str = DATA_FILE
) -> None:
    response:Response = api_client.post(
        path=api_endpoint,
        data={'file':open(filename)},
        format='multipart'
    )

    expected_original_df = pd.read_csv(DATA_FILE)
    expected_original_df_json = expected_original_df.to_json(orient='records')


    assert expected_original_df_json == response.data['original_data']['original_data_json']