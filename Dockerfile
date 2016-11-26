FROM python:3.5-slim
MAINTAINER crisbal cristian@baldi.me

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y curl wget

#we do this because we can't run worker as root
RUN groupadd worker && useradd --create-home --home-dir /worker -g worker worker

WORKDIR /tmp
RUN wget https://github.com/jgm/pandoc/releases/download/1.17.2/pandoc-1.17.2-1-amd64.deb -O /tmp/pandoc.deb \
    && dpkg -i /tmp/pandoc.deb \
    && apt-get install -f
RUN apt-get install -y calibre

WORKDIR /worker

# celery requirements, pretty stable
ADD requirements.txt .
RUN pip install -r requirements.txt

USER worker

ADD . .

ENTRYPOINT ["celery"]
CMD ["-A", "tasks", "worker", "-l", "INFO", "-Q", "eg"]