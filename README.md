# python

## Start compose environment

- TBD

## Build and run

```bash
$ docker build -t "python-app" "env/build/python/."
$ docker run -it --rm --name "name" "python-app"
```

## Run a single Python script with default image

For many simple, single file projects, you may find it inconvenient to write a complete Dockerfile. In such cases, you can run a Python script by using the Python Docker image directly:

```bash
$ docker run -it --rm --name "name" -v "$(pwd)/src:/usr/src/app" -w "/usr/src/app" python:3 python your-daemon-or-script.py
```

## One liners

### Windows

Build and run a specific hello-world.py:

```powershell
docker build -t "python-dev" "env/dev/build/python/."; docker run -it --rm -v "$(pwd)/src:/usr/src/app" "python-dev" python hello-world.py
```

```bash
docker build -t "python-dev" "env/dev/build/python/." && docker run -it --rm -v "$(pwd)/src:/usr/src/app" "python-dev" python hello-world.py
```
