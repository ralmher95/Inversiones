# 📊 Proyecto de Optimización Cuantitativa de Carteras

Análisis financiero y construcción de carteras de inversión multi-activo utilizando **Python**, **Yahoo Finance** y técnicas de **optimización de Markowitz** mediante **simulación Monte Carlo**.

El proyecto cubre tres perfiles de riesgo —conservador, equilibrado y arriesgado— y genera de forma automática gráficos profesionales (Sharpe, correlaciones, frontera eficiente) e informes en formato Word con las ponderaciones óptimas calculadas en tiempo real.

---

## 🎯 Objetivos

- Obtener datos reales de mercado (ETFs, REITs, Bitcoin ETC) directamente desde Yahoo Finance.
- Calcular métricas financieras clave: rentabilidad anualizada, volatilidad, máximo drawdown, ratio de Sharpe y matriz de correlación.
- Optimizar cada cartera para **máximo Sharpe** y **mínima volatilidad** utilizando Monte Carlo (50.000 carteras aleatorias) sin depender de librerías externas de optimización.
- Generar gráficos responsive (adaptables a móvil) con estilo *dark mode* profesional.
- Producir informes en Word automáticos que incluyen tanto los pesos típicos de referencia como los pesos óptimos calculados con los datos del día de ejecución.

---

## 📁 Estructura del proyecto

| Archivo | Descripción |
|--------|-------------|
| `inversionConservadora.py` | Análisis individual de activos conservadores (Sharpe, correlaciones, barras y heatmap). |
| `inversionEquilibrado.py` | Análisis individual de activos equilibrados (Sharpe, correlaciones, barras y heatmap). |
| `inversionArriesgada.py` | Análisis individual de activos arriesgados (Sharpe, correlaciones, barras y heatmap). |
| `markowitzConservadora.py` | Frontera eficiente y optimización Monte Carlo para el perfil conservador. |
| `markowitzEquilibrado.py` | Frontera eficiente y optimización Monte Carlo para el perfil equilibrado. |
| `markowitzArriesgada.py` | Frontera eficiente y optimización Monte Carlo para el perfil arriesgado. |
| `informe_conservador_word.py` | Genera informe Word con métricas, pesos orientativos y pesos reales (conservador). |
| `informe_equilibrado.py` | Genera informe Word con métricas, pesos orientativos y pesos reales (equilibrado). |
| `Informe_Arriesgado.py` | Genera informe Word con métricas, pesos orientativos y pesos reales (arriesgado). |

*Los archivos `.docx` no se versionan — solo se incluye el código fuente.*

---

## 🧰 Activos utilizados por perfil

### Conservador (7 ETFs)
`Global Bonds (EUNA.DE)`, `MSCI World (XMWO.DE)`, `Min Volatility (IQQ0.DE)`, `Emerging Markets (IS3N.DE)`, `Physical Gold (SGLD.L)`, `Developed World (VHVG.L)`, `Inflation Linked (IBEI.DE)`.

### Equilibrado (5 ETFs)
`MSCI World (XMWO.DE)`, `Emerging Markets (IS3N.DE)`, `Global REITs (IUSP.DE)`, `Global Bonds (EUNA.DE)`, `Physical Gold (SGLD.L)`.

### Arriesgado (5 activos)
`S&P 500 (CSPX.L)`, `Info Tech Sector (QDVE.DE)`, `World Small Cap (IUSN.DE)`, `Emerging Markets (IS3N.DE)`, `Bitcoin ETC (BTCE.DE)`.

> **Nota:** Los tickers que fallen o estén *delisted* se eliminan automáticamente. La optimización se realiza siempre con los activos que tengan al menos 100 días de datos.

---

## 🚀 Ejecución

1. Clonar el repositorio e instalar las dependencias:
   ```bash
   git clone https://github.com/ralmher95/Inversiones.git
   cd Inversiones
   pip install -r requirements.txt
   ```

2. Ejecuta los script en el siguiente orden:
   ```bash
   python inversionConservadora.py
   python inversionEquilibrado.py
   python inversionArriesgada.py
   python markowitzConservadora.py
   python markowitzEquilibrado.py
   python markowitzArriesgada.py
   python informe_conservador_word.py
   python informe_equilibrado.py
   python Informe_Arriesgado.py
   ```

3. Los informes (`.docx`) se generarán automáticamente en la carpeta del proyecto.