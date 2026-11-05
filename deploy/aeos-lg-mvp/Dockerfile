FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd -m -u 10001 app && mkdir -p /tmp/lg && chown -R app:app /tmp/lg
COPY --chown=app:app app.py .
USER app
ENV LG_DB_PATH=/tmp/lg/leads.db
EXPOSE 10000
CMD ["sh","-c","uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000} --workers 1"]
