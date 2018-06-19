FROM phusion/baseimage

WORKDIR /app

RUN apt-get update &&  \
    apt-get install -y \
      curl \
      git-core \
      mysql-client \
      python-mysqldb \
      python-pip \
      vim && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD bash -c 'tail -f requirements.txt'
