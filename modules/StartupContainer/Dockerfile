FROM python:3-stretch

EXPOSE 8082

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-u", "./main.py" ]