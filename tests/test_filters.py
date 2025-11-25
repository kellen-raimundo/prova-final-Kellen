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
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["total"] = df["preco"] * df["quantidade"]

    app.df = df
    return app

def test_filter_by_year():
    app = setup_app()

    app.cbo_ano.set("2023")
    app.cbo_categoria.set("(Todas)")
    app.cbo_produto.set("(Todos)")

    app.aplicar_filtros()

    assert all(app.filtered_df["ano"] == 2023)

def test_filter_by_category():
    app = setup_app()

    app.cbo_ano.set("(Todos)")
    app.cbo_categoria.set("Gamer")
    app.cbo_produto.set("(Todos)")

    app.aplicar_filtros()

    assert all(app.filtered_df["categoria"] == "Gamer")

def test_filter_by_product():
    app = setup_app()

    app.cbo_ano.set("(Todos)")
    app.cbo_categoria.set("(Todas)")
    app.cbo_produto.set("Mouse Pro")

    app.aplicar_filtros()

    assert all(app.filtered_df["produto"] == "Mouse Pro")
