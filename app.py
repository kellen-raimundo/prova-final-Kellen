import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
import matplotlib

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardVendasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard de Vendas - Python + Pandas + Tkinter")
        self.root.geometry("1100x650")

        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.canvas = None

        self._build_layout()

    def _build_layout(self):
        top_frame = ttk.Frame(self.root, padding=5)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        btn_carregar = ttk.Button(top_frame, text="Carregar dados(csv)", command=self.carregar_dados)
        btn_carregar.pack(side=tk.LEFT, padx=5)

        btn_relatorio = ttk.Button(top_frame, text="Gerar Relatório", command=self.gerar_relatorio)
        btn_relatorio.pack(side=tk.LEFT, padx=5)

        filtro_frame = ttk.LabelFrame(self.root, text="Filtros", padding=5)
        filtro_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(filtro_frame, text="Ano: ").pack(side=tk.LEFT, padx=5)
        self.cbo_ano = ttk.Combobox(filtro_frame, state="readonly", width=10)
        self.cbo_ano.pack(side=tk.LEFT)

        ttk.Label(filtro_frame, text="Categoria:").pack(side=tk.LEFT, padx=5)
        self.cbo_categoria = ttk.Combobox(filtro_frame, state="readonly", width=15)
        self.cbo_categoria.pack(side=tk.LEFT)

        ttk.Label(filtro_frame, text="Produto: ").pack(side=tk.LEFT, padx=5)
        self.cbo_produto = ttk.Combobox(filtro_frame, state="readonly", width=20)
        self.cbo_produto.pack(side=tk.LEFT)

        btn_aplicar = ttk.Button(filtro_frame, text="Aplicar Filtros", command=self.aplicar_filtros)
        btn_aplicar.pack(side=tk.LEFT, padx=10)

        btn_limpar = ttk.Button(filtro_frame, text="Limpar Filtros", command=self.limpar_filtros)
        btn_limpar.pack(side=tk.LEFT)

        main_frame = ttk.Frame(self.root, padding=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tabela_frame = ttk.Frame(main_frame)
        tabela_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tabela_frame, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(yscrollcommand=vsb.set)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stats_frame = ttk.LabelFrame(right_frame, text="Estatísticas", padding=5)
        stats_frame.pack(fill=tk.X)

        self.txt_stats = tk.Text(stats_frame, height=8, width=40)
        self.txt_stats.pack(fill=tk.X)

        rel_frame = ttk.LabelFrame(right_frame, text="Relatório", padding=5)
        rel_frame.pack(fill=tk.BOTH, expand=True)

        self.txt_relatorio = tk.Text(rel_frame, height=10, width=40)
        self.txt_relatorio.pack(fill=tk.BOTH, expand=True)

        graficos_frame = ttk.LabelFrame(right_frame, text="Graficos", padding=5)
        graficos_frame.pack(fill=tk.BOTH, expand=True)

        btn_cat = ttk.Button(graficos_frame, text="Vendas por Categoria", command=self.plot_vendas_por_categoria)
        btn_cat.pack(fill=tk.X, pady=2)

        btn_mes = ttk.Button(graficos_frame, text="Vendas por Mês", command=self.plot_vendas_por_mes)
        btn_mes.pack(fill=tk.X, pady=2)

        btn_top5 = ttk.Button(graficos_frame, text="Top 5 Produtos", command=self.plot_top5_produtos)
        btn_top5.pack(fill=tk.X, pady=2)

        self.grafico_container = ttk.Frame(graficos_frame)
        self.grafico_container.pack(fill=tk.BOTH, expand=True)

    def carregar_dados(self):
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo de vendas",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
        )
        if not filepath:
            return
        try:
            df = pd.read_csv(filepath)
            df = df.dropna(subset=["preco", "quantidade", "data", "produto", "categoria"])
            df["preco"] = pd.to_numeric(df["preco"], errors="coerce")
            df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
            df["data"] = pd.to_datetime(df["data"], errors="coerce")
            df = df.dropna(subset=["preco", "quantidade", "data"])
            df["total"] = df["preco"] * df["quantidade"]
            df["ano"] = df["data"].dt.year
            df["mes"] = df["data"].dt.month

            self.df = df
            self.filtered_df = df.copy()

            self.atualizar_comboxes()
            self.mostrar_dataframe(self.filtered_df)
            self.mostrar_estatisticas(self.filtered_df)
            self.txt_relatorio.delete("1.0", tk.END)

            messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar: {e}")

    def atualizar_comboxes(self):
        anos = sorted(self.df["ano"].unique().tolist())
        categorias = sorted(self.df["categoria"].unique().tolist())
        produtos = sorted(self.df["produto"].unique().tolist())

        self.cbo_ano["values"] = ["(Todos)"] + [str(a) for a in anos]
        self.cbo_categoria["values"] = ["(Todas)"] + categorias
        self.cbo_produto["values"] = ["(Todos)"] + produtos

    def aplicar_filtros(self):
        df = self.df.copy()
        ano = self.cbo_ano.get()
        categoria = self.cbo_categoria.get()
        produto = self.cbo_produto.get()

        if ano != "(Todos)":
            df = df[df["ano"] == int(ano)]
        if categoria != "(Todas)":
            df = df[df["categoria"] == categoria]
        if produto != "(Todos)":
            df = df[df["produto"] == produto]

        self.filtered_df = df
        self.mostrar_dataframe(df)
        self.mostrar_estatisticas(df)

    def limpar_filtros(self):
        self.filtered_df = self.df.copy()
        self.mostrar_dataframe(self.filtered_df)
        self.mostrar_estatisticas(self.filtered_df)

    def mostrar_dataframe(self, df):
        for col in self.tree.get_children():
            self.tree.delete(col)
        self.tree["columns"] = list(df.columns)

        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def calcular_estatisticas(self, df):
        stats = {}
        stats["faturamento_total"] = df["total"].sum()
        stats["faturamento_medio"] = df["total"].mean()
        stats["faturamento_mediana"] = df["total"].median()
        stats["faturamento_max"] = df["total"].max()
        stats["faturamento_min"] = df["total"].min()
        stats["quantidade_total_vendida"] = df["quantidade"].sum()
        stats["top5"] = df.groupby("produto")["total"].sum().nlargest(5)
        return stats

    def mostrar_estatisticas(self, df):
        self.txt_stats.delete("1.0", tk.END)
        stats = self.calcular_estatisticas(df)
        for k, v in stats.items():
            if k != "top5":
                self.txt_stats.insert(tk.END, f"{k}: {v}")
        self.txt_stats.insert(tk.END, "Top 5 produtos")
        for p, v in stats["top5"].items():
            self.txt_stats.insert(tk.END, f"{p}: {v}")

    def gerar_relatorio(self):
        rel = "RELATÓRIO DE VENDAS"
        rel += "="*40 + ""
        df = self.filtered_df
        stats = self.calcular_estatisticas(df)
        rel += f"Registros: {len(df)}"
        rel += f"Periodo: {df['data'].min().date()} até {df['data'].max().date()}"
        rel += f"Faturamento Total: {stats['faturamento_total']}"
        rel +=  f"Faturamento Médio: {stats['faturamento_medio']}"
        rel += f"Top 5 produtos:"
        for p, v in stats["top5"].items():
            rel += f"- {p}: {v}"
        self.txt_relatorio.delete(1.0, tk.END)
        self.txt_relatorio.insert(tk.END, rel)

    def _limpar_canvas(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

    def plot_vendas_por_categoria(self):
        df = self.filtered_df
        dados = df.groupby("categoria")["total"].sum()
        fig = Figure(figsize=(4,3))
        ax = fig.add_subplot(111)
        dados.plot(kind="bar", ax=ax)
        ax.set_title("Vendas por Categoria")
        self._limpar_canvas()
        self.canvas = FigureCanvasTkAgg(fig, master=self.grafico_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_vendas_por_mes(self):
        df = self.filtered_df
        dados = df.groupby("mes")["total"].sum()
        fig = Figure(figsize=(4, 3))
        ax = fig.add_subplot(111)
        dados.plot(kind="bar", ax=ax)
        ax.set_title("Vendas por Mês")
        self._limpar_canvas()
        self.canvas = FigureCanvasTkAgg(fig, master=self.grafico_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_top5_produtos(self):
        df = self.filtered_df
        dados = df.groupby("produto")["total"].sum().nlargest(5)
        fig = Figure(figsize=(4, 3))
        ax = fig.add_subplot(111)
        dados.plot(kind="bar", ax=ax)
        ax.set_title("Top 5 Produtos por Faturamento")
        self._limpar_canvas()
        self.canvas = FigureCanvasTkAgg(fig, master=self.grafico_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

