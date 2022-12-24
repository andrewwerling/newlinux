# install mariaDB server
FROM ubuntu
RUN sudo apt-get update && apt-get install -y mariadb-connector-c
RUN sudo apt install libmariadb3 libmariadb-dev
RUN sudo apt-install mariadb-server
RUN sudo service mariadb enable
ENV MARIADB_CONFIG /usr/bin/mariadb_config

# start by pulling the python image
FROM python:3.10-alpine
# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -U pip
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["view.py" ]