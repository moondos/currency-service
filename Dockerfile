FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y build-essential
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "./currency_service.py", "--currencies", "KZT", "UZS", "AZN", "MYR", "--ds", "2024-05-31"]
