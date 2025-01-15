# Backend README

## Descripción
Este proyecto es un backend desarrollado en Flask, que se conecta a una base de datos PostgreSQL. Aquí encontrarás las instrucciones para configurar el entorno, instalar dependencias, configurar la base de datos y ejecutar la aplicación localmente.

---

## Requisitos previos
Asegúrate de tener instalados los siguientes elementos en tu sistema:

- **Python 3.10 o superior**
- **PostgreSQL**
- **Git**

---

## Configuración del entorno de desarrollo

### 1. Clonar el repositorio
```bash
git clone https://github.com/No-Country-simulation/c23-92-T-webapp.git
cd c23-92-T-webapp/backend
```

### 2. Crear y activar un entorno virtual
En el directorio raíz del proyecto, ejecuta:

**Linux/MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
Una vez activado el entorno virtual, instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

---

## Configuración de la base de datos

### 1. Crear la base de datos en PostgreSQL
Accede a tu terminal de PostgreSQL o herramienta como pgAdmin y ejecuta:

```sql
CREATE DATABASE c23_92_t_webapp;
```

### 2. Configurar el archivo `.env`
Copia el archivo `.env.example` y renómbralo como `.env`:

```bash
cp .env.example .env
```

Luego, edita el archivo `.env` para incluir tus credenciales de la base de datos:

```plaintext
DATABASE_URL=postgresql://<usuario>:<contraseña>@localhost:5432/c23_92_t_webapp
```
- Reemplaza `<usuario>` y `<contraseña>` con los datos de tu base de datos.

---

## Migraciones de la base de datos
Este proyecto utiliza **Flask-Migrate** para manejar las migraciones de la base de datos.

### 1. Inicializar las migraciones (solo la primera vez)
```bash
flask db init
```

### 2. Crear un archivo de migración después de modificar los modelos
```bash
flask db migrate -m "Descripción de los cambios"
```

### 3. Aplicar las migraciones a la base de datos
```bash
flask db upgrade
```

---

## Ejecutar la aplicación

### 1. Configurar `.flaskenv` (opcional para desarrollo)
Crea un archivo `.flaskenv` en el directorio raíz del proyecto con las siguientes líneas:

```plaintext
FLASK_APP=app.py
FLASK_ENV=development
```

### 2. Ejecutar la aplicación
Con el entorno virtual activado, corre el servidor:

```bash
flask run
```

La aplicación estará disponible en: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Estructura del proyecto
```plaintext
c23-92-T-webapp/
    ├── .env.example        # Plantilla para variables de entorno
    ├── .env                # Variables de entorno sensibles (ignorado por Git)
    ├── .flaskenv           # Configuración para desarrollo
    └── backend/
        ├── app.py              # Archivo principal del servidor Flask
        ├── models.py           # Definición de modelos de base de datos
        ├── migrations/         # Carpeta generada por Flask-Migrate para las migraciones
        ├── requirements.txt    # Lista de dependencias del proyecto
        └── README.md           # Instrucciones del proyecto
```

---

## Notas adicionales
- **Asegúrate de no incluir los archivos `.env` y `.flaskenv` en tu repositorio público.** Están listados en `.gitignore` para proteger tu información sensible.
- Si necesitas actualizar los paquetes en `requirements.txt`, utiliza:

```bash
pip freeze > requirements.txt
```

---


