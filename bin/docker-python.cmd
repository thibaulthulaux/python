@ECHO OFF
cd ..
ECHO # Building python-dev
docker build^
  -t "python-dev"^
  "env/dev/build/python/."
ECHO # Running python %*
docker run -it --rm^
  -v "%CD%/app/src:/app/src"^
  "python-dev"^
  python %*