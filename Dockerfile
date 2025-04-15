FROM python:latest

WORKDIR /app

#RUN apt update && install -y libgtk-3-dev

COPY requirements.txt ./

RUN pip install -U pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["flet", "run", "main.py"]
