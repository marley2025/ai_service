FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (uncomment if you later need build tools)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential && \
#     rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the app (keeps image smaller & rebuilds faster)
COPY ai_quoting ./ai_quoting

EXPOSE 8080

CMD ["uvicorn", "ai_quoting.app:app", "--host", "0.0.0.0", "--port", "8080"]
