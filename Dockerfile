FROM python:3.11-slim
<<<<<<< HEAD
#Docker File Python Version 3.11
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip  --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000


CMD ["python","app.py"]


=======
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
>>>>>>> origin/main

