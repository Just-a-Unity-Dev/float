FROM python:3.11

WORKDIR /app
COPY REQUIREMENTS.txt ./

ENV TOKEN=secret

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./main.py"]