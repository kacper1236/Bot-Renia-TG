# Twój własny obraz bazowy
FROM python:3.14-slim

# Instalacja wszystkich zależności systemowych, które zawsze są potrzebne
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev \
        gcc \
        python3-dev \
        build-essential \
        libpq-dev \
        libffi-dev \
        python3-dev \
        curl \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g nodemon \
    && apt-get clean && rm -rf /var/lib/apt/lists/*