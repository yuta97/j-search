FROM python:3.7


# ADD . /root
COPY . /opt
WORKDIR /opt

RUN pip install -r requirements.txt