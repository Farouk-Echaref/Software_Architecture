FROM python:3.10-slim-bullseye

RUN sed -i 's|http://deb.debian.org|http://ftp.fr.debian.org|g' /etc/apt/sources.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
     build-essential default-libmysqlclient-dev pkg-config \
  && pip install --no-cache-dir --upgrade pip


WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 5000

CMD ["python3", "server.py"]