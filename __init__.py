import pandas as pd
from app import DashboardVendasApp

def test_dataframe_loading():
    df = pd.read_csv("tests/vendas_2000.csv")
    assert not df.empty
    assert "preco" in df.columns
    assert "quantidade" in df.columns
