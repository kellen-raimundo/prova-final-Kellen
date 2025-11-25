import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
import pandas as pd
from app import DashboardVendasApp

def setup_app():
    root = tk.Tk(); root.withdraw()
    app = DashboardVendasApp(root)

    df = pd.read_csv("vendas_2000.csv")
    df["data"] = pd.to_datetime(df["data"])
    df["mes"] = df["data"].dt.month
    df["total"] = df["preco"] * df["quantidade"]
    app.filtered_df = df

    return app

def test_plot_mes():
    app = setup_app()
    try:
        app.plot_vendas_por_mes()
    except Exception as e:
        assert False, f"Erro ao gerar gráfico por mês: {e}"
