FROM blendergrid/blender:2.91

ENV PYTHONUNBUFFERED=1

RUN apt-get update
    
RUN apt-get install python3.9 python3-pip -y \
    && pip3 install --upgrade pip setuptools

WORKDIR /app
COPY . /app/

RUN ./packages.sh

RUN python3 manage.py collectstatic --no-input

RUN python3 manage.py makemigrations \
    && python3 manage.py migrate

RUN ln -s /app/effects /app/static

CMD ["daphne", "-b", "0.0.0.0", "-p", "9090", "work.asgi:application"]
