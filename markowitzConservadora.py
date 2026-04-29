"""
Optimización de Cartera - Frontera Eficiente (5 activos, responsive)
======================================================================
Requisitos: pip install yfinance pandas numpy matplotlib scipy
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ── CONFIGURACIÓN (5 ACTIVOS) ──
ACTIVOS = {
    "IS3N.DE": "Emerging Markets",
    "EUNA.DE": "Global Bonds",
    "XMWO.DE": "MSCI World Swap",
    "IQQ0.DE": "Min Volatility",
    "SGLD.L": "Physical Gold",
}
TICKERS = list(ACTIVOS.keys())
TASA_RF = 0.0315
N_DIAS = 252
PERIODO = "3y"

print("⬇ Descargando datos históricos...")
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
returns = data.pct_change().dropna()
n = len(activos_ok)
print(f"✅ Activos disponibles: {activos_ok}\n")

# ── Función de estadísticas de cartera ──
def stats_cartera(weights):
    weights = np.array(weights)
    port_returns = returns.dot(weights)
    ret_anual = port_returns.mean() * N_DIAS
    vol_anual = port_returns.std() * np.sqrt(N_DIAS)
    if vol_anual == 0:
        return np.nan, np.nan, np.nan
    sharpe = (ret_anual - TASA_RF) / vol_anual
    return ret_anual, vol_anual, sharpe

# ── Optimización ──
cons = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
bounds = tuple((0, 1) for _ in range(n))
init = np.ones(n) / n

opt_sharpe = minimize(lambda w: -stats_cartera(w)[2], init,
                      method="SLSQP", bounds=bounds, constraints=cons)
opt_vol    = minimize(lambda w: stats_cartera(w)[1], init,
                      method="SLSQP", bounds=bounds, constraints=cons)

res_ms = stats_cartera(opt_sharpe.x)
res_mv = stats_cartera(opt_vol.x)

# ── Monte Carlo ──
num_portfolios = 5000
mc_ret = np.zeros(num_portfolios)
mc_vol = np.zeros(num_portfolios)
mc_sr  = np.zeros(num_portfolios)

for i in range(num_portfolios):
    w = np.random.random(n)
    w /= np.sum(w)
    r, v, s = stats_cartera(w)
    mc_ret[i] = r
    mc_vol[i] = v
    mc_sr[i]  = s

# ── Visualización responsiva ──
BG = "#0A0C12"
FG = "#E8E4DC"

fig, ax = plt.subplots(figsize=(16, 9))   # más alto y ancho
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

sc = ax.scatter(mc_vol * 100, mc_ret * 100, c=mc_sr, cmap="viridis",
                marker="o", s=10, alpha=0.4, edgecolors="none", zorder=2)
cbar = plt.colorbar(sc, ax=ax, pad=0.02)
cbar.set_label("Ratio de Sharpe", color=FG, fontsize=11)
cbar.ax.yaxis.set_tick_params(color=FG)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=FG)

ax.scatter(res_ms[1] * 100, res_ms[0] * 100, marker="*", color="#E05555",
           s=600, zorder=5, edgecolors="white", linewidth=1.5,
           label=f'Máx. Sharpe ({res_ms[2]:.2f})')
ax.scatter(res_mv[1] * 100, res_mv[0] * 100, marker="*", color="#4EC9C0",
           s=600, zorder=5, edgecolors="white", linewidth=1.5,
           label=f'Mín. Volatilidad ({res_mv[1]*100:.2f}%)')

# Anotaciones con más separación
ax.annotate(
    f'Sharpe: {res_ms[2]:.2f}\nRet: {res_ms[0]*100:.1f}%\nVol: {res_ms[1]*100:.1f}%',
    xy=(res_ms[1]*100, res_ms[0]*100),
    xytext=(25, 25), textcoords='offset points',
    color=FG, fontsize=9, fontfamily='monospace',
    bbox=dict(boxstyle='round,pad=0.5', facecolor=BG, edgecolor=FG, alpha=0.9),
    arrowprops=dict(arrowstyle='->', color=FG, lw=1.5)
)
ax.annotate(
    f'Sharpe: {res_mv[2]:.2f}\nRet: {res_mv[0]*100:.1f}%\nVol: {res_mv[1]*100:.1f}%',
    xy=(res_mv[1]*100, res_mv[0]*100),
    xytext=(-90, -45), textcoords='offset points',
    color=FG, fontsize=9, fontfamily='monospace',
    bbox=dict(boxstyle='round,pad=0.5', facecolor=BG, edgecolor=FG, alpha=0.9),
    arrowprops=dict(arrowstyle='->', color=FG, lw=1.5)
)

ax.set_title("Frontera Eficiente de Markowitz — 5 Activos Conservadores",
             color=FG, fontsize=15, fontweight="bold", pad=20)
ax.set_xlabel("Volatilidad Anualizada (%)", color=FG, fontsize=12, labelpad=10)
ax.set_ylabel("Retorno Anualizado Esperado (%)", color=FG, fontsize=12, labelpad=10)
ax.tick_params(colors=FG, labelsize=10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_color("#2A3050")
ax.spines["left"].set_color("#2A3050")
ax.grid(True, alpha=0.2, color=FG, linestyle="--")
ax.legend(loc="upper left", facecolor="#171C28", edgecolor="#2A3050",
          labelcolor=FG, fontsize=11, framealpha=0.9)

fig.text(0.01, 0.01,
         f"RF BCE: {TASA_RF*100:.2f}%  ·  {num_portfolios:,} carteras  ·  "
         f"Período: {PERIODO}  ·  {datetime.now().strftime('%Y-%m-%d')}",
         color=FG, fontsize=8, alpha=0.6, fontfamily="monospace")

plt.tight_layout(pad=2)
plt.savefig("frontera_eficiente_5.png", dpi=200, bbox_inches="tight", facecolor=BG)
plt.show()

# ── Resultados en consola ──
print("\n─── CARTERA MÁXIMO SHARPE ──────────────────────────")
print(f"  Retorno esperado : {res_ms[0]*100:.2f}%")
print(f"  Volatilidad      : {res_ms[1]*100:.2f}%")
print(f"  Sharpe Ratio     : {res_ms[2]:.3f}\n")
for i, ticker in enumerate(activos_ok):
    peso = opt_sharpe.x[i] * 100
    if peso > 0.1:
        print(f"  {ACTIVOS.get(ticker, ticker):<22} {peso:5.1f}%")

print("\n─── CARTERA MÍNIMA VOLATILIDAD ─────────────────────")
print(f"  Retorno esperado : {res_mv[0]*100:.2f}%")
print(f"  Volatilidad      : {res_mv[1]*100:.2f}%")
print(f"  Sharpe Ratio     : {res_mv[2]:.3f}\n")
for i, ticker in enumerate(activos_ok):
    peso = opt_vol.x[i] * 100
    if peso > 0.1:
        print(f"  {ACTIVOS.get(ticker, ticker):<22} {peso:5.1f}%")

print("\n✅  Gráfico guardado como frontera_eficiente_5.png")