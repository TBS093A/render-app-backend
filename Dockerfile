FROM python:3

ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip setuptools

RUN apt-get update
RUN apt-get install blender -y

WORKDIR /app
COPY . /app/

RUN ./packages.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:9090"]