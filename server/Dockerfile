FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN mkdir -p /api/src/
WORKDIR /api/src/
COPY requirements.txt /api/src/requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT [ "flask" ]
CMD [ "run", "--host=0.0.0.0", "--port=4000" ]