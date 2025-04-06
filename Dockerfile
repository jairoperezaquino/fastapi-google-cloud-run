FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=True

ENV APP_HOME=/app
WORKDIR ${APP_HOME}

RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

CMD ["sh", "-c", "exec fastapi run app/main.py --port ${PORT:-8080}"]