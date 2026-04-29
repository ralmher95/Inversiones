"""
Análisis de Cartera Conservadora Global (5 activos - Responsive)
==================================================================
Requisitos: pip install yfinance pandas seaborn matplotlib numpy
"""

import pandas as pd
import numpy as np
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import sys
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class AnalizadorCartera:
    def __init__(self, tasa_rf=0.0315, periodo="3y"):
        # ── 5 ACTIVOS CONSERVADORES ──
        self.ACTIVOS = {
    "IS3N.DE": "Emerging Markets",
    "EUNA.DE": "Global Bonds",
    "EUNL.DE": "MSCI World",          
    "IQQ0.DE": "Min Volatility",
    "SGLD.L": "Physical Gold",
}
        self.TICKERS = list(self.ACTIVOS.keys())
        self.TASA_RF = tasa_rf
        self.PERIODO = periodo
        self.N_DIAS = 252

        self.COLORES = {
            'BG': "#0A0C12", 'FG': "#E8E4DC", 'GRID': "#171C28",
            'TEAL': "#4EC9C0", 'RED': "#E05555", 'GOLD': "#D4A847"
        }

        self.data = None
        self.retornos = None
        self.activos_ok = None
        self.nombres_ok = None
        self.df_sharpe = None
        self.matriz_corr = None

    def descargar_datos(self):
        print("⬇ Descargando datos...")
        try:
            raw = yf.download(
                self.TICKERS, period=self.PERIODO,
                auto_adjust=True, progress=False
            )
        except Exception as e:
            print(f"❌ Error descargando datos: {e}")
            sys.exit(1)

        if "Close" not in raw.columns:
            data = raw.dropna(axis=1, how='all')
        else:
            data = raw["Close"].dropna(axis=1, how='all')

        min_dias = 100
        self.activos_ok = [t for t in data.columns if data[t].notna().sum() >= min_dias]
        if len(self.activos_ok) < 2:
            raise ValueError("Se necesitan al menos 2 activos con datos.")
        self.data = data[self.activos_ok]
        self.nombres_ok = [self.ACTIVOS.get(t, t) for t in self.activos_ok]

        print(f"✅ Activos disponibles ({len(self.activos_ok)}/{len(self.TICKERS)}):")
        for t in self.activos_ok:
            print(f"   • {t}: {self.ACTIVOS.get(t, 'Desconocido')}")
        print()

    def calcular_retornos(self):
        if self.data is None:
            self.descargar_datos()
        self.retornos = self.data.pct_change().dropna()
        if self.retornos.empty:
            raise ValueError("No se pudieron calcular retornos")

    def calcular_metricas(self):
        if self.retornos is None:
            self.calcular_retornos()

        ret_anual = self.retornos.mean() * self.N_DIAS
        vol_anual = self.retornos.std() * np.sqrt(self.N_DIAS)
        sharpe = (ret_anual - self.TASA_RF) / vol_anual

        cummax = self.data.cummax()
        drawdown = (self.data - cummax) / cummax
        max_dd = drawdown.min()

        self.df_sharpe = pd.DataFrame({
            "Nombre": self.nombres_ok,
            "Ret. anual (%)": (ret_anual * 100).round(2),
            "Vol. anual (%)": (vol_anual * 100).round(2),
            "Max Drawdown (%)": (max_dd * 100).round(2),
            "Sharpe Ratio": sharpe.round(3),
        }, index=self.activos_ok)

        self.matriz_corr = self.retornos.corr()

    def mostrar_resultados_consola(self):
        if self.df_sharpe is None:
            self.calcular_metricas()
        print("── Sharpe Ratio (anualizado, RF = {:.2f}%) ──".format(self.TASA_RF * 100))
        print(self.df_sharpe.sort_values("Sharpe Ratio", ascending=False).to_string())
        print()
        print("── Matriz de Correlación ──")
        matriz_named = self.matriz_corr.copy()
        matriz_named.columns = self.nombres_ok
        matriz_named.index = self.nombres_ok
        print(matriz_named.round(3).to_string())
        mejor = self.df_sharpe.loc[self.df_sharpe["Sharpe Ratio"].idxmax()]
        print(f"\n🏆 Mejor Sharpe: {mejor['Nombre']} ({mejor['Sharpe Ratio']:.2f})")

    def visualizar(self, guardar=True):
        if self.df_sharpe is None:
            self.calcular_metricas()

        BG = self.COLORES['BG']
        FG = self.COLORES['FG']
        GRID = self.COLORES['GRID']
        TEAL = self.COLORES['TEAL']
        RED = self.COLORES['RED']
        GOLD = self.COLORES['GOLD']

        plt.style.use("dark_background")
        fig = plt.figure(figsize=(20, 10), facecolor=BG)
        gs = gridspec.GridSpec(
            1, 2, figure=fig, width_ratios=[1, 1.4],
            wspace=0.15, left=0.05, right=0.97,
            top=0.88, bottom=0.12
        )

        # Panel izquierdo: Barras Sharpe
        ax1 = fig.add_subplot(gs[0])
        ax1.set_facecolor(BG)

        vals = self.df_sharpe["Sharpe Ratio"].values
        y_pos = np.arange(len(self.activos_ok))
        etiquetas = [f"{t}\n{self.ACTIVOS.get(t, t)}" for t in self.activos_ok]
        colores = [TEAL if v >= 1 else ("#6A8EAE" if v >= 0 else RED) for v in vals]

        bars = ax1.barh(y_pos, vals, color=colores, height=0.5, zorder=3)
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(etiquetas, color=FG, fontsize=9, fontfamily="monospace")
        ax1.axvline(0, color=FG, lw=0.7, alpha=0.35, zorder=2)
        ax1.axvline(1.0, color=TEAL, lw=1.0, alpha=0.55, linestyle="--", zorder=2)
        ax1.axvline(0.5, color=GOLD, lw=0.8, alpha=0.40, linestyle=":", zorder=2)

        for bar, val in zip(bars, vals):
            offset = 0.05 if val >= 0 else -0.05
            ax1.text(val + offset, bar.get_y() + bar.get_height()/2,
                     f"{val:+.2f}", va="center", ha="left" if val >= 0 else "right",
                     color=FG, fontsize=10, fontfamily="monospace", fontweight="bold")

        x_min, x_max = ax1.get_xlim()
        for i, ticker in enumerate(self.activos_ok):
            ret = self.df_sharpe.loc[ticker, "Ret. anual (%)"]
            vol = self.df_sharpe.loc[ticker, "Vol. anual (%)"]
            mdd = self.df_sharpe.loc[ticker, "Max Drawdown (%)"]
            ax1.text(x_min + 0.02*(x_max - x_min), i - 0.35,
                     f"ret {ret:+.1f}%  vol {vol:.1f}%  dd {mdd:.1f}%",
                     color=FG, fontsize=7, alpha=0.55,
                     fontfamily="monospace", va="center")

        ax1.set_xlabel(f"Sharpe Ratio (anualizado · RF = {self.TASA_RF*100:.2f}%)",
                       color=FG, labelpad=6, fontsize=10)
        ax1.set_title("Sharpe Ratio por activo", color=FG, fontsize=13,
                      fontweight="bold", loc="left", pad=12)
        ax1.tick_params(axis="x", colors=FG, labelsize=8)
        ax1.tick_params(axis="y", length=0)
        for spine in ax1.spines.values():
            spine.set_visible(False)
        ax1.grid(axis="x", color=GRID, lw=0.8, zorder=0)
        ax1.legend(loc='lower right', framealpha=0.1, fontsize=7,
                   labelcolor=FG, facecolor=BG)

        # Panel derecho: Mapa de Calor
        ax2 = fig.add_subplot(gs[1])
        ax2.set_facecolor(BG)

        matriz_named = self.matriz_corr.copy()
        matriz_named.columns = self.nombres_ok
        matriz_named.index = self.nombres_ok

        cmap = LinearSegmentedColormap.from_list("rg", [RED, "#1A2035", TEAL], N=256)

        sns.heatmap(
            matriz_named,
            annot=True, cmap=cmap, center=0, vmin=-1, vmax=1,
            fmt=".2f", square=True, ax=ax2,
            linewidths=0.6, linecolor=BG,
            annot_kws={"size": 10, "color": FG, "family": "monospace", "weight": "bold"},
            cbar_kws={"shrink": 0.75, "pad": 0.02},
        )

        ax2.set_title("Matriz de Correlación\n(retornos diarios · 3 años)",
                      color=FG, fontsize=13, fontweight="bold", loc="left", pad=12)
        ax2.tick_params(colors=FG, labelsize=9, length=0)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=35, ha="right",
                            color=FG, fontfamily="monospace", fontsize=9)
        ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0,
                            color=FG, fontfamily="monospace", fontsize=9)

        cbar = ax2.collections[0].colorbar
        cbar.ax.tick_params(colors=FG, labelsize=8)
        cbar.outline.set_edgecolor(GRID)

        fig.suptitle("Cartera Conservadora Global (5 activos) · Riesgo/Retorno",
                     color=FG, fontsize=16, fontweight="bold", y=0.98)

        fig.text(0.01, 0.01,
                 f"RF BCE: {self.TASA_RF*100:.2f}% · Anualización √{self.N_DIAS} · "
                 f"Período: {self.PERIODO} · {datetime.now().strftime('%Y-%m-%d')}",
                 color=FG, fontsize=7.5, alpha=0.5, fontfamily="monospace")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        if guardar:
            plt.savefig("cartera_conservadora.png", dpi=200,
                        bbox_inches="tight", facecolor=BG)
            print("✅ Gráfico guardado como cartera_conservadora.png")
        plt.show()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("📊 ANÁLISIS DE CARTERA CONSERVADORA GLOBAL (5 ACTIVOS)")
    print("="*60 + "\n")
    analizador = AnalizadorCartera(tasa_rf=0.0315, periodo="3y")
    analizador.descargar_datos()
    analizador.calcular_metricas()
    analizador.mostrar_resultados_consola()
    analizador.visualizar(guardar=True)
    print("\n✅ Análisis completado exitosamente")