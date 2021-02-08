# FROM nytimes/blender:2.91-gpu-ubuntu18.04
FROM python:3.9

ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip setuptools

WORKDIR /app
COPY . /app/

RUN ./packages.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:9090"]