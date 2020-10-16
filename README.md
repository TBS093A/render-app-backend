# Render App
Python / Django REST Framework / Django Channels REST Framework / Gevent / Blender

## Basic informations

Application for rendering images of hand gestures in cycles (blender) like in photogrammetry. You can use rendered sets for ML algorithm training - sign language recognize for example

## Install

### Install blender package

Install blender for server functionality

```bash

sudo apt-get install blender

```

### Create Python Environment and install requirment packages

Create envirionment

```bash

python3 -m venv venv

```

Install packages automatically

```bash

./packages.sh

```

## Usage

### Migrate All Application Tables

```bash

./migrate.sh

```

### Run Tests

```bash

./test.sh

```

### Run Server

```bash

./run.sh

```

### Show Celery Workers / Tasks

```bash

./celery.sh

```