FROM python:3.11 

WORKDIR /web_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /web_app

