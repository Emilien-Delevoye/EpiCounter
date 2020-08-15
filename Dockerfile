FROM python:3.7-slim
COPY . /app
WORKDIR /app

RUN apt-get update && \
        apt-get install -yq --no-install-recommends \
                        postgresql-server-dev-all \
                        gcc python3-dev musl-dev && \
        apt-get clean && \
        rm -rf /var/lib/apt/list

RUN pip3 install -r requirements.txt

CMD ["python", "app.py"]