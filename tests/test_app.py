import requests
import pytest
from src.config import API_KEY, CONN_URL
from sqlalchemy import create_engine

# Test DB connection
@pytest.mark.parametrize("conn_url", [CONN_URL])
def test_db(conn_url):
    engine = create_engine(conn_url, echo=False)
    response_db = engine == 200
    return response_db


# Test API
@pytest.mark.parametrize("symbol,API_KEY", [("BTC", API_KEY), ("ETH", API_KEY)])
def test_api(symbol, API_KEY):
    url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&apikey={API_KEY}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.content != None
    assert response.json()["Meta Data"]["2. Digital Currency Code"] == symbol


# # Force failing task to check Github actions
# def test_failing():
#     assert 1 == 2
