FROM nginx:stable
LABEL maintainer="Thibault <thibault.hulaux@gmail.com>" \
      description="tomcat"

USER root

COPY nginx.conf /etc/nginx/nginx.conf
RUN chmod 644 /etc/nginx/nginx.conf
# RUN chown root:root /etc/nginx/nginx.conf
COPY tomcat.conf /etc/nginx/conf.d/tomcat.conf
RUN chmod 644 /etc/nginx/conf.d/tomcat.conf
# RUN chown root:root /etc/nginx/conf.d/tomcat.conf


