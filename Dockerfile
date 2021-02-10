FROM python:3

ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip setuptools

RUN apt-get update

RUN wget http://us.download.nvidia.com/tesla/418.87/nvidia-driver-local-repo-ubuntu1804-418.87.01_1.0-1_amd64.deb \
    && dpkg -i nvidia-driver-local-repo-ubuntu1804-418.87.01_1.0-1_amd64.deb \
    && apt-key add /var/nvidia-driver-local-repo-418.87.01/7fa2af80.pub \
    && dpkg -i nvidia-driver-local-repo-ubuntu1804-418.87.01_1.0-1_amd64.deb

# RUN apt install cuda-drivers -y

RUN apt-get install blender -y

RUN apt-get install libgl1-mesa-glx \
    libxi6 libxrender1 freeglut3 \
    freeglut3-dev libxi-dev libxmu-dev -y

WORKDIR /app
COPY . /app/

RUN ./packages.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:9090"]