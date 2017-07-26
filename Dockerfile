FROM python:3.6.1-slim

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python","manage.py","testserver","test.json","--addrport","0.0.0.0:8000"]