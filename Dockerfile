FROM python:3.10

ENV workdir=/app
RUN mkdir -p $workdir
WORKDIR $workdir
RUN apt-get update
RUN apt-get install -y openssl ca-certificates
RUN apt-get install -y libffi-dev build-essential libssl-dev git rustc cargo  software-properties-common
RUN echo "deb https://notesalexp.org/tesseract-ocr5/$(lsb_release -cs)/ $(lsb_release -cs) main" \
    | tee /etc/apt/sources.list.d/notesalexp.list > /dev/null
RUN wget -O - https://notesalexp.org/debian/alexp_key.asc | apt-key add -
RUN apt update && \
    apt install -y tesseract-ocr \
    tesseract-ocr-deu \
    tesseract-ocr-fra  \
    tesseract-ocr-eng \
    poppler-utils


RUN pip3 install pip -U
RUN pip3 install poetry -U
COPY poetry.lock $workdir
COPY pyproject.toml $workdir
RUN poetry install --no-root --only=main

RUN rm -rf /root/.cargo
# COPY code later in the layers (after dependencies are installed)
# It builds the containers 2x faster on code change
COPY . $workdir
# Most of dependencies are already installed, it only install the app
RUN poetry install --only=main

RUN apt-get remove --purge -y libffi-dev build-essential libssl-dev git rustc cargo

ENV PROMETHEUS_MULTIPROC_DIR=/tmp/opticr/prometheus
