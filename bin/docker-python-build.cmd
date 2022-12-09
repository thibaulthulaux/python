@ECHO OFF
cd ..
ECHO # Building python-dev
docker build^
  -t "python-dev"^
  "env/dev/build/python/."