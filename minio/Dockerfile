FROM ubuntu:24.04

COPY minio /usr/local/bin/minio

RUN chmod +x /usr/local/bin/minio

EXPOSE 9000 9001

ENTRYPOINT ["minio"]
