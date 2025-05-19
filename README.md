# GeoVelocity API

API desarrollada en **FastAPI** para análisis y comparación de sesiones geográficas usando clustering y métricas de movimiento.

---

## Requisitos

- Python **3.9**
- Git
- curl o PowerShell

---

## 🐍 Instalación de Python 3.9

### 🔧 En Windows

1. Ir a [https://www.python.org/downloads/release/python-390/](https://www.python.org/downloads/release/python-390/)
2. Descargar el instalador de Windows (ej: `Windows installer (64-bit)`)
3. Ejecutar el instalador y **activar la opción** ✅ `Add Python to PATH`
4. Finalizar la instalación

Verificá la instalación con:

```bash
python --version
```

---

## 📦 Instalación de Poetry

### 🚀 Configuración del entorno con Poetry

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

## 📁 Clonar este repositorio

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

## 🧩 Instalar dependencias del proyecto

```bash
poetry install
```

## 🌐 Ejecutar la API

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```