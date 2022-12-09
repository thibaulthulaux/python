@ECHO OFF
cd ..
ECHO # Running python %*
docker run -it --rm^
  -v "%CD%/app/src:/app/src"^
  "python-dev"^
  python %*