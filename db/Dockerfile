FROM postgres:12

ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

RUN mkdir /src
WORKDIR /src
COPY test.db .
WORKDIR /

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
                    git \
                    locate \
                    nano && \
    apt-get clean && \
    rm -rf /var/lib/apt/list


ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8