# 📊 Proyecto de Optimización Cuantitativa de Carteras

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Source: Yahoo Finance](https://img.shields.io/badge/Data-Yahoo%20Finance-purple)](https://finance.yahoo.com/)

Análisis financiero y construcción de carteras multi-activo utilizando **Python**, **Yahoo Finance** y la **optimización de Markowitz** mediante **simulación Monte Carlo** (50.000 carteras aleatorias). El proyecto cubre tres perfiles de riesgo —conservador, equilibrado y arriesgado— y genera automáticamente:

- Gráficos profesionales (frontera eficiente, ratio de Sharpe, mapa de correlaciones, rentabilidad vs volatilidad).
- Informes en formato Word con las ponderaciones **teóricas de referencia** y las **óptimas calculadas en tiempo real** con los datos del día de ejecución.

> 🎓 **Nota:** Este proyecto tiene fines **educativos y de investigación**. No constituye asesoramiento financiero. Los resultados dependen de datos históricos y no garantizan rentabilidades futuras.

---

## 📑 Tabla de contenidos

- [Objetivos](#-objetivos)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Activos por perfil de riesgo](#-activos-utilizados-por-perfil)
- [Requisitos e instalación](#-requisitos-e-instalación)
- [Ejecución paso a paso](#-ejecución)
- [Resultados esperados](#-resultados-esperados)
- [Limitaciones y deuda técnica](#-limitaciones-y-deuda-técnica)
- [Mejoras futuras](#-mejoras-futuras)
- [Licencia](#-licencia)

---

## 🎯 Objetivos

- Descargar **datos reales de mercado** (ETFs, REITs, Bitcoin ETC) desde Yahoo Finance.
- Calcular métricas financieras clave:  
  `rentabilidad anualizada`, `volatilidad anualizada`, `máximo drawdown`, `ratio de Sharpe`, `matriz de correlación`.
- Optimizar cada cartera para **máximo Sharpe** y **mínima volatilidad** usando Monte Carlo (sin depender de librerías externas de optimización como `scipy.optimize`).
- Generar gráficos **responsive** (adaptables a móvil) con estilo *dark mode* profesional.
- Producir informes en Word que incluyan tanto los **pesos orientativos iniciales** como los **pesos óptimos** basados en los datos del día de ejecución.

---

## 📁 Estructura del proyecto

| Archivo | Descripción |
|---------|-------------|
| `inversionConservadora.py` | Análisis individual de activos conservadores (Sharpe, correlaciones, barras y heatmap). |
| `inversionEquilibrado.py` | Análisis individual de activos equilibrados (idem). |
| `inversionArriesgada.py` | Análisis individual de activos arriesgados (idem). |
| `markowitzConservadora.py` | Frontera eficiente y optimización Monte Carlo para el perfil conservador. |
| `markowitzEquilibrado.py` | Frontera eficiente y optimización Monte Carlo para el perfil equilibrado. |
| `markowitzArriesgada.py` | Frontera eficiente y optimización Monte Carlo para el perfil arriesgado. |
| `informe_conservador.py` | Genera informe Word con métricas, pesos orientativos y pesos reales (conservador). |
| `informe_equilibrado.py` | Genera informe Word para el perfil equilibrado. |
| `informe_arriesgado.py` | Genera informe Word para el perfil arriesgado. |

*Los archivos `.docx` no se versionan — solo se incluye el código fuente.*

> 💡 **Sugerencia:** Puedes agrupar toda la ejecución en un script `main.py` que llame a estos módulos en orden. Por simplicidad, aquí se ejecutan individualmente.

---

## 🧰 Activos utilizados por perfil

### 🛡️ Conservador (7 ETFs)
- `Global Bonds (EUNA.DE)`
- `MSCI World (XMWO.DE)`
- `Min Volatility (IQQ0.DE)`
- `Emerging Markets (IS3N.DE)`
- `Physical Gold (SGLD.L)`
- `Developed World (VHVG.L)`
- `Inflation Linked (IBEI.DE)`

### ⚖️ Equilibrado (5 ETFs)
- `MSCI World (XMWO.DE)`
- `Emerging Markets (IS3N.DE)`
- `Global REITs (IUSP.DE)`
- `Global Bonds (EUNA.DE)`
- `Physical Gold (SGLD.L)`

### 🚀 Arriesgado (5 activos)
- `S&P 500 (CSPX.L)`
- `Info Tech Sector (QDVE.DE)`
- `World Small Cap (IUSN.DE)`
- `Emerging Markets (IS3N.DE)`
- `Bitcoin ETC (BTCE.DE)`

> **Nota:** Los tickers que fallen o estén *delisted* se eliminan automáticamente. La optimización solo se ejecuta con activos que tengan al menos **100 días de datos históricos**.

---

## 🔧 Requisitos e instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/ralmher95/Inversiones.git
   cd Inversiones

2. **Crear un entorno virtual (recomendado)**
```bash 
python -m venv venv
```

```bash
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```



---

## 🚀 Ejecución

# Ejecuta los scripts en el siguiente orden para cada perfil.

### Análisis individual de activos
```bash
python inversionConservadora.py
python inversionEquilibrado.py
python inversionArriesgada.py
```

# Optimización de cartera (Markowitz + Monte Carlo)
```bash
python markowitzConservadora.py
python markowitzEquilibrado.py
python markowitzArriesgada.py
```

### Generación de informes Word
```bash
python informe_conservador.py
python informe_equilibrado.py
python informe_arriesgado.py
```

## 📈 Resultados esperados

### Gráficos generados:

- Frontera eficiente con 50.000 carteras simuladas.

- Ratio de Sharpe vs volatilidad.

- Heatmap de correlación entre activos.

- Diagrama de barras de pesos óptimos.

### Informe Word que incluye:

- Tabla con rentabilidad, volatilidad, Sharpe y drawdown de cada activo.
- Pesos orientativos (referencia inicial) y pesos óptimos calculados.
- Composición final de la cartera (máximo Sharpe y mínima varianza).


## ⚠️ Limitaciones y deuda técnica

- Los informes en Word podrían ser más interactivos (por ejemplo, generar un dashboard HTML o un PDF interactivo).
- Se podría añadir un análisis de más gráficos por perfil y visualización de riesgo (VaR, CVaR).
- No se incluye gestión de errores completa ni un entorno más robusto para producción.

## 🧪 Mejoras futuras

- Script unificado main.py con argumentos (--perfil, --simulaciones).
- Soporte para más fuentes de datos (Alpha Vantage, Polygon.io).
- Exportación a Excel y PDF además de Word.
- Optimización con restricciones personalizadas (sector, liquidez, ESG).
- Integración con backtesting fuera de muestra.
- Panel interactivo con Streamlit o Dash.

## 📄 Licencia

- Este proyecto se distribuye bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente, siempre que se incluya el aviso de copyright original. Ver el archivo LICENSE para más detalles.

## ✍️ Autor y contacto

- [Ralmher95 – GitHub](https://github.com/ralmher95)

- Proyecto original: [Inversiones](https://github.com/ralmher95/Inversiones)

- ¿Comentarios o sugerencias? Abre un issue o un pull request. ¡Toda ayuda es bienvenida!