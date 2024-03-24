import pytest
from rest_framework.test import APIClient
from rest_framework import status
from data_cleansing_server.urls import DATATYPE_ENDPOINT
from datatype.urls import INFER_ENDPOINT

@pytest.fixture(scope='session')
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def api_endpoint() -> str:
    return f"/{DATATYPE_ENDPOINT}{INFER_ENDPOINT}"