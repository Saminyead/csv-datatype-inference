import pytest
from rest_framework.test import APIClient
from rest_framework.response import Response


INVALID_FILE:str = './files/invalid.pdf'
DATA_FILE:str = './files/data.csv'


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
def test_api_data_file_format(
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
        assert value in response.data['inferred_data_types']

    