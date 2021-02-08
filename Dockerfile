FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app/

RUN ./packages.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:9090"]