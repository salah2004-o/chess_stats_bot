FROM python:3.12-slim

WORKDIR /Chess_stats_bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]