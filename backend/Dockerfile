FROM python:3.12.3

ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_APP=app.py

WORKDIR /app

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