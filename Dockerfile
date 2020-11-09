FROM python:3.6

ENV CONTAINER_NAME=/var/www

WORKDIR ${CONTAINER_NAME}

RUN apt-get update 
RUN pip install --upgrade pip
RUN pip install psycopg2-binary

ADD requirements.txt ${CONTAINER_NAME}
ADD src/ ${CONTAINER_NAME}

RUN pip install --no-cache-dir -r requirements.txt
