FROM resin/rpi-raspbian:jessie

WORKDIR /app
EXPOSE 8080

# Install dependencies
RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        wget \
        build-essential \
        libjpeg-dev \
        python3-dev \
        zlib1g-dev 
    
COPY requirements.txt ./
RUN pip3 install --upgrade pip 
RUN pip install --upgrade setuptools 
RUN pip install -r requirements.txt
RUN pip install http://ci.tensorflow.org/view/Nightly/job/nightly-pi-python3/179/artifact/output-artifacts/tensorflow-1.7.0-cp34-none-any.whl

COPY . /app/

ENTRYPOINT [ "python3", "main.py" ]
