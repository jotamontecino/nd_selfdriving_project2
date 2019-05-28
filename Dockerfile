FROM debian:stretch-slim

ENV PYTHONPATH=/app/src \
    PYTHON_VERSION=3 \
    PYTHON_BOILERPLATE_ACTION=start \
    PYTHON_BOILERPLATE_TASK_DIR=/etc/python-boilerplate/ \
    RUNNING_ON_DOCKER=true \
    WSGI_APPLICATION=app \
    STATIC_FILES=/var/www/


# Install dependencies and create folders

RUN mkdir /app/ &&\
    mkdir /var/www/ &&\
    \
    # Install apt dependencies
    apt-get update &&\
    apt-get install --no-install-recommends --no-install-suggests -y \
            libglib2.0-0 \
            libsm6 \
            libxext6 \
            libxrender-dev \
            curl \
            python3 \
            python3-pip \
            python3-setuptools \
            python3-wheel \
            python3-pytest \
            python3-pytest-cov \
            python3-jinja2 \
            python3-unidecode &&\
    rm -rf /var/lib/apt/lists/*


# Install python-boilerplate from pip

RUN pip3 install python-boilerplate &&\
    rm ~/.pip/cache -rf


# You should install everything under the /app/ directory

WORKDIR /app/
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

CMD python3 main.py
