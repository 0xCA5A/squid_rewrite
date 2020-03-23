FROM debian:buster
LABEL maintainer="samuel.casa@bluecare.ch"

RUN apt-get update \
 && apt install -y squid apache2-utils wget imagemagick python3 \
 && rm -rf /var/lib/apt/lists/*

# This variable are used by start script entrypoint.sh
ENV SQUID_CACHE_DIR=/var/spool/squid \
    SQUID_LOG_DIR=/var/log/squid \
    SQUID_CFG_FILE=/etc/squid/squid.conf \
    SQUID_REWRITE_DIR=/var/log/squid/rewrite \
    SQUID_USER=proxy \
    SQUID_EXTRA_ARGS=""

COPY entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh

# Place the squid rewrite handler script
RUN mkdir -p /etc/squid3/scripts/
COPY rewrite.py /etc/squid3/scripts/rewrite.py
RUN chmod 755 /etc/squid3/scripts/rewrite.py

# NOTE: The port has to match your Squid config, 3128 is the default
EXPOSE 3128/tcp
ENTRYPOINT ["/sbin/entrypoint.sh"]