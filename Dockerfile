FROM python:3.11
FROM igloo/float_bot:latest

WORKDIR /app
COPY REQUIREMENTS.txt ./

ENV TOKEN=secret

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r REQUIREMENTS.txt

COPY . .

CMD ["python", "./main.py"]