FROM python:3.12-slim

WORKDIR /app

# Install deps first (better layer caching — deps rarely change, code changes often)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

# Not running as root, small good habit
RUN useradd -m appuser
USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]