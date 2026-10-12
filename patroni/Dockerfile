FROM postgres:16

RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        pgbackrest && \
    pip3 install --no-cache-dir --break-system-packages \
        "patroni[etcd3]" \
        psycopg2-binary && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["patroni", "/etc/patroni.yml"]
