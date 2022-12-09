# FROM mariadb:latest
# mariadb:latest requires docker version 20.10.10+ but
# boot2docker comes with Docker version 19.03.12, build 48a66213fe
FROM mariadb:10.8.2
LABEL maintainer="Thibault <thibault.hulaux@gmail.com>" \
      description="mariadb"

COPY initdb /docker-entrypoint-initdb.d

# RUN echo "default-authentication-plugin=mysql_native_password" >> /etc/mysql/my.cnf

# https://www.devopsschool.com/blog/install-and-configure-prometheus-mysql-exporter/

# # Update apt.
# RUN apt -y update
# 
# # Install extra packets.
# RUN apt -y install \
#     curl \
#     daemonize \
#     git \
#     wget
# 
# # Clean up.
# RUN rm -rf /var/cache/apt/* && \
#     rm -rf /var/lib/apt/lists/* && \
#     apt clean
# 
# # Add Prometheus user
# RUN groupadd --system promotheus && \
#     useradd -s /sbin/nologin --system -g promotheus promotheus
# 
# # Install Prometheus MySQL Exporter
# RUN curl -s https://api.github.com/repos/prometheus/mysqld_exporter/releases/latest \
#     | grep browser_download_url \
#     | grep linux-amd64 \
#     | cut -d '"' -f 4 \
#     | wget -qi - && \
#     tar xvf mysqld_exporter*.tar.gz && \
#     mv  mysqld_exporter-*.linux-amd64/mysqld_exporter /usr/local/bin/ && \
#     chmod +x /usr/local/bin/mysqld_exporter

# RUN git clone https://github.com/jmutai/prometheus-mysqld-exporter-init-script.git && \
#     cd prometheus-mysqld-exporter-init-script && \
#     chmod +x mysqld_exporter.init && \
#     mv mysqld_exporter.init /etc/init.d/mysqld_exporter


# Confirm installation by checking version of mysqld_exporter
# $ mysqld_exporter  --version

# Copying and running start script.
# COPY /start.sh /start.sh
# CMD ["/bin/bash", "/start.sh"]



