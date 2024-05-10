FROM mysql:latest

ENV MYSQL_DATABASE campus_care
ENV MYSQL_ROOT_PASSWORD team37

ADD schema.sql /docker-entrypoint-initdb.d

EXPOSE 3306
