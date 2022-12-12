FROM python:3

LABEL maintainer="Thibault HULAUX <thibault.hulaux@gmail.com>" \
      description="Python environment"

# WORKDIR /usr/src/app
WORKDIR /app/src

COPY "requirements.txt" "./"
RUN pip install --no-cache-dir -r requirements.txt

# COPY "../" "."

# CMD [ "python", "hello-world.py" ]
# CMD [ "ls", "-al" ]