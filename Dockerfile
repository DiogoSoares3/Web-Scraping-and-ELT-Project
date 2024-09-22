FROM python:3.10

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /PROJECT

COPY . /PROJECT

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]