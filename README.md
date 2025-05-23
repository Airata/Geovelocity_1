# GeoVelocity API

API desarrollada en **FastAPI** para análisis y comparación de sesiones geográficas usando clustering y métricas de movimiento.

## Instalación:

### Requisitos

- Python **3.9**
- Git
- curl o PowerShell

### 🐍 Instalación de Python 3.9

#### 🔧 En Windows

1. Ir a [https://www.python.org/downloads/release/python-390/](https://www.python.org/downloads/release/python-390/)
2. Descargar el instalador de Windows (ej: `Windows installer (64-bit)`)
3. Ejecutar el instalador y **activar la opción** ✅ `Add Python to PATH`
4. Finalizar la instalación

Verificá la instalación con:

```bash
python --version
```

### 📦 Instalación de Poetry

**🚀 Configuración del entorno con Poetry**

Este proyecto utiliza [**Poetry**](https://python-poetry.org/) para la gestión de dependencias y entornos virtuales en Python.

A continuación, te mostramos cómo instalar Poetry.

#### 🔧 Método universal recomendado: En macOS / Linux / Windows (con `curl`):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verificá la instalación con:

```bash
poetry --version
```

### 📁 Clonar este repositorio

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

### 🧩 Instalar dependencias del proyecto

```bash
poetry install
```

### 🌐 Ejecutar la API

```bash
poetry run python main.py
```

## 📡 API Endpoints

La API expone los siguientes endpoints para análisis de sesiones geográficas y clustering:

### 🔍 **Health checks**

|Método|Endpoint|Descripción|
|---|---|---|
|`GET`|`/health`|Verifica que la API esté en funcionamiento.|
|`GET`|`/health/velocity`|Ejecuta una comparación simulada de sesiones (métrica de geovelocidad).|
|`GET`|`/health/cluster`|Ejecuta un clustering simulado de sesiones y lo categoriza.|

---

### 🚦 **Comparación de sesiones**

|Método|Endpoint|Descripción|
|---|---|---|
|`POST`|`/velocity/compare-last`|Compara una nueva sesión con la última sesión conocida del usuario.|
|`POST`|`/velocity/compare-all`|Compara una lista de sesiones consecutivas y calcula distancia, tiempo y velocidad entre cada par.|

---

### 🧭 **Clustering geográfico**

|Método|Endpoint|Descripción|
|---|---|---|
|`POST`|`/geo/cluster-categorize`|Aplica clustering (DBSCAN) a una lista de sesiones y clasifica cada una como `principal`, `secundario` o `ruido`.|

---

