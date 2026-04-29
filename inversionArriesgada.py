"""
Análisis Cartera Arriesgada Global - Responsive
Sharpe · Correlación · Drawdown · Barras y Heatmap
====================================================
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

ACTIVOS = {
    "CSPX.L": "S&P 500",
    "QDVE.DE": "Info Tech Sector",
    "IUSN.DE": "World Small Cap",
    "IS3N.DE": "Emerging Markets",
    "BTCE.DE": "Bitcoin ETC",
}
TICKERS = list(ACTIVOS.keys())
TASA_RF = 0.0315
N_DIAS = 252
PERIODO = "3y"

print("⬇ Descargando datos...")
raw = yf.download(TICKERS, period=PERIODO, auto_adjust=True, progress=False)

if "Close" not in raw.columns:
    data = raw.dropna(axis=1, how='all')
else:
    data = raw["Close"].dropna(axis=1, how='all')

min_dias = 100
activos_ok = [t for t in data.columns if data[t].notna().sum() >= min_dias]
if len(activos_ok) < 2:
    raise ValueError("Se necesitan al menos 2 activos con datos.")

data = data[activos_ok]
nombres_ok = [ACTIVOS.get(t, t) for t in activos_ok]
retornos = data.pct_change().dropna()
print(f"✅ Activos disponibles: {activos_ok}\n")

ret_anual = retornos.mean() * N_DIAS
vol_anual = retornos.std() * np.sqrt(N_DIAS)
sharpe = (ret_anual - TASA_RF) / vol_anual
max_dd = ((data / data.cummax()) - 1).min()

df_sharpe = pd.DataFrame({
    "Nombre": nombres_ok,
    "Ret. anual (%)": (ret_anual * 100).round(2),
    "Vol. anual (%)": (vol_anual * 100).round(2),
    "Max Drawdown (%)": (max_dd * 100).round(2),
    "Sharpe Ratio": sharpe.round(3),
}, index=activos_ok)

print(df_sharpe.sort_values("Sharpe Ratio", ascending=False).to_string(), "\n")

matriz_corr = retornos.corr()
matriz_named = matriz_corr.copy()
matriz_named.columns = nombres_ok
matriz_named.index = nombres_ok
print(matriz_named.round(2).to_string(), "\n")

# ── VISUALIZACIÓN RESPONSIVA ──
BG, FG, GRID = "#0A0C12", "#E8E4DC", "#171C28"
TEAL, RED, GOLD = "#4EC9C0", "#E05555", "#D4A847"

plt.style.use("dark_background")
fig = plt.figure(figsize=(20, 10), facecolor=BG)
gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1, 1.4],
                        wspace=0.15, left=0.05, right=0.97,
                        top=0.88, bottom=0.12)

# Panel izquierdo
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor(BG)
vals = df_sharpe["Sharpe Ratio"].values
y_pos = np.arange(len(activos_ok))
etiquetas = [f"{t}\n{ACTIVOS.get(t, t)}" for t in activos_ok]
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
for i, ticker in enumerate(activos_ok):
    ret = df_sharpe.loc[ticker, "Ret. anual (%)"]
    vol = df_sharpe.loc[ticker, "Vol. anual (%)"]
    mdd = df_sharpe.loc[ticker, "Max Drawdown (%)"]
    ax1.text(x_min + 0.02*(x_max - x_min), i - 0.35,
             f"ret {ret:+.1f}%  vol {vol:.1f}%  dd {mdd:.1f}%",
             color=FG, fontsize=7, alpha=0.55, fontfamily="monospace", va="center")

ax1.set_xlabel(f"Sharpe Ratio (anualizado · RF = {TASA_RF*100:.2f}%)",
               color=FG, labelpad=6, fontsize=10)
ax1.set_title("Sharpe Ratio por activo", color=FG, fontsize=13,
              fontweight="bold", loc="left", pad=12)
ax1.tick_params(axis="x", colors=FG, labelsize=8)
ax1.tick_params(axis="y", length=0)
ax1.spines[:].set_visible(False)
ax1.grid(axis="x", color=GRID, lw=0.8, zorder=0)

# Panel derecho
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(BG)
cmap = LinearSegmentedColormap.from_list("rg", [RED, "#1A2035", TEAL], N=256)

sns.heatmap(
    matriz_named, annot=True, cmap=cmap, center=0, vmin=-1, vmax=1,
    fmt=".2f", square=True, ax=ax2, linewidths=0.6, linecolor=BG,
    annot_kws={"size": 10, "color": FG, "family": "monospace", "weight": "bold"},
    cbar_kws={"shrink": 0.75, "pad": 0.02}
)

ax2.set_title("Matriz de Correlación (retornos diarios · 3 años)",
              color=FG, fontsize=13, fontweight="bold", loc="left", pad=12)
ax2.tick_params(colors=FG, labelsize=9, length=0)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=35, ha="right",
                    color=FG, fontfamily="monospace", fontsize=9)
ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0,
                    color=FG, fontfamily="monospace", fontsize=9)
cbar = ax2.collections[0].colorbar
cbar.ax.tick_params(colors=FG, labelsize=8)
cbar.outline.set_edgecolor(GRID)

fig.suptitle("Cartera Arriesgada Global · Riesgo/Retorno",
             color=FG, fontsize=16, fontweight="bold", y=0.98)

fig.text(0.01, 0.01,
         f"RF BCE: {TASA_RF*100:.2f}% · Anualización √{N_DIAS} · "
         f"Período: {PERIODO} · {datetime.now().strftime('%Y-%m-%d')}",
         color=FG, fontsize=7.5, alpha=0.5, fontfamily="monospace")

plt.savefig("cartera_arriesgada_sharpe.png", dpi=200, bbox_inches="tight", facecolor=BG)
plt.show()
print("✅ Gráfico guardado como cartera_arriesgada_sharpe.png")