# FROM tomcat:9
# tomcat:9 requires docker version 20.10.10+ but
# boot2docker comes with Docker version 19.03.12, build 48a66213fe
FROM tomcat:9-jdk11-temurin-focal
LABEL maintainer="Thibault <thibault.hulaux@gmail.com>" \
      description="tomcat"

# USER root

# Set root password.
RUN echo 'root:root' | chpasswd

# Update apt.
RUN apt -y update

# Install openssh-server.
RUN apt -y install openssh-server && \
    mkdir -p /var/run/sshd && \
    sed -ri 's/#Port 22/Port 55022/g' /etc/ssh/sshd_config && \
    sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config && \
    sed -ri 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config && \
    sed -ri 's/#PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    echo "$0:$?: /etc/ssh/ssh_config edited."

# Clean up.
RUN rm -rf /var/cache/apt/* && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean

# Copy default webapps
# RUN cp -rv webapps.dist/* webapps/

COPY jaas.config /usr/local/tomcat/conf/jaas.config

# Copying and running start script.
COPY /start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]

# Default run
# docker run -it --rm -p 8888:8080 tomcat:9.0

# Default env
# CATALINA_BASE:   /usr/local/tomcat
# CATALINA_HOME:   /usr/local/tomcat
# CATALINA_TMPDIR: /usr/local/tomcat/temp
# JRE_HOME:        /usr
# CLASSPATH:       /usr/local/tomcat/bin/bootstrap.jar:/usr/local/tomcat/bin/tomcat-juli.jar
