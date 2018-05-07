FROM debian:jessie

WORKDIR /app
EXPOSE 8080

# Install dependencies
RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        libjpeg-dev python-scipy \
        wget 

COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install tensorflow

COPY . .

CMD [ "python3", "./main.py" ]
