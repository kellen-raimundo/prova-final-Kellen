import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
import pandas as pd
from app import DashboardVendasApp

def prepare_df():
    df = pd.read_csv("vendas_2000.csv")
    df["data"] = pd.to_datetime(df["data"])
    df["total"] = df["preco"] * df["quantidade"]
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    return df

def test_stats_basic(monkeypatch):
    # evita abrir janela real
    root = tk.Tk(); root.withdraw()
    app = DashboardVendasApp(root)

    df = prepare_df()
    stats = app.calcular_estatisticas(df)

    assert stats["faturamento_total"] > 0
    assert stats["quantidade_total_vendida"] > 0
