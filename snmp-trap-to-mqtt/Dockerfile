ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3

# Install pip for python3
RUN \
  apk add --no-cache \
    py3-pip

# Install what we need to build python packages (gcc, musl-dev, python3-dev)
RUN \
  apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev

# Install python requirements for add-on
COPY requirements.txt /tmp/

RUN \
  pip3 install --no-cache-dir -r /tmp/requirements.txt \
  && rm -f /tmp/requirements.txt

WORKDIR /data

COPY main.py /data/

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]