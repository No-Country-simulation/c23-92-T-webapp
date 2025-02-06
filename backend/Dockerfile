FROM python:3.12.3

ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_APP=app.py \
    SECRET_KEY=c%Q|1Q"oz59V*c/o\xpN~"@{rgG4Udg| \
    REFRESH_SECRET_KEY=Mts,1Tf>_;=T>o\*&^}{gS/G7C**rF*/Q/4&(J)+(Azn(+fd@J*JJgkIzCS#{@%_ \
    REFRESH_ENCRYPTION_KEY=aJtxgzlzRee_avClSIRCiPyHQc1uNPyMEV-Bi-ELhAI= \
    OPENAI_API_KEY=sk-ZAsVF7ryr1V5aKgcMqychRZrUqvo68qmGLqICOb_MlT3BlbkFJRvVRrbLdLSqCKGaG1DNUPgRx85z5-Z7JUkBcIwxZ8A \
    DB_USERNAME="avnadmin" \
    DB_PASSWORD="AVNS_R6wazrcWz0qIbyGX_5v" \
    DB_HOST="mia-service-mia-project.g.aivencloud.com" \
    DB_PORT="19200" \
    DB_NAME="mia_database" \
    COOKIE_SECRET_KEY=qNdL2VH1K2cPHrAZVXPdP2PExXcFGPXkGAah1qiVKW0=

WORKDIR /app

# Instala las dependencias del sistema necesarias para compilar Pillow y otras librerías
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    zlib1g-dev \
    libpq-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY src/ ./src/
COPY app.py ./
COPY extensions.py ./
COPY secret_key.py ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
