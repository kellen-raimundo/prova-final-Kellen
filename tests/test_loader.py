import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import os

def test_csv_exists():
    assert os.path.exists("vendas_2000.csv"), "Arquivo vendas_2000.csv não encontrado!"

def test_csv_structure():
    df = pd.read_csv("vendas_2000.csv")

    required = ["id_venda", "data", "produto", "categoria", "preco", "quantidade"]
    for col in required:
        assert col in df.columns, f"Coluna obrigatória ausente: {col}"

def test_csv_data_types():
    df = pd.read_csv("vendas_2000.csv")

    assert df["preco"].dtype in ("float64", "float32"), "Preço deve ser float"
    assert df["quantidade"].dtype in ("int64", "int32"), "Quantidade deve ser int"
