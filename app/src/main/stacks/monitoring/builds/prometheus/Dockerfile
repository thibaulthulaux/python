FROM prom/prometheus:main
LABEL maintainer="Thibault <thibault.hulaux@gmail.com>" \
      description="prometheus"

USER root

COPY prometheus.yaml /etc/prometheus/prometheus.yml
COPY alerts.yaml /etc/prometheus/alerts.yml
 
RUN chown nobody:nobody /etc/prometheus/prometheus.yml

