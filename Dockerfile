FROM ubuntu:20.04

RUN apt-get upgrade && apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
  && apt-get install -y libpq-dev gdal-bin python3-pip python3-dev libcogl-pango-dev  libcairo2-dev  python3-venv \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && rm -fr /var/lib/apt/lists/*

WORKDIR /project

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install --upgrade setuptools && \
    pip3 install -r requirements.txt

EXPOSE 8000

CMD [ "bash", "boot.sh" ]
