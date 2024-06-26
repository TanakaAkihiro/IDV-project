FROM python:3.10-slim

WORKDIR /usr/src/app

EXPOSE 8050

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8050", "--reload", "app:server"]