FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .


RUN pip install --no-cache-dir --upgrade pip setuptools == 78.1.1  && \
    pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

EXPOSE 5000


CMD ["python","app.py"]



