FROM resin/rpi-raspbian:jessie

EXPOSE 8082

# disable python buffering to console out (https://docs.python.org/2/using/cmdline.html#envvar-PYTHONUNBUFFERED)
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
    apt-utils \
    python-picamera \
    python-smbus \
    python-setuptools \
    python-dev \
    python-pil \
    libjpeg8-dev \
    zlib1g-dev \
    i2c-tools \
    libcurl4-openssl-dev \
    python-pip \
    wget

# RUN wget -qO- https://bootstrap.pypa.io/get-pip.py | python

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app/

ENTRYPOINT [ "python", "main.py" ]
