# FROM python:3
# FROM forwardcomputers/blender:2.91.2
FROM blendergrid/blender:2.91

ENV PYTHONUNBUFFERED=1

# RUN apk update
# RUN apk add --no-cache python3 py3-pip

RUN apt-get update
    
RUN apt-get install python3.9 python3-pip -y \
    && pip3 install --upgrade pip setuptools

WORKDIR /app
COPY . /app/

RUN ./packages.sh

RUN python3 manage.py collectstatic --no-input

RUN ln -s /app/effects /app/static

# CMD ["python", "manage.py", "runserver", "0.0.0.0:9090"]
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9090", "work.asgi"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "9090", "work.asgi:application"]